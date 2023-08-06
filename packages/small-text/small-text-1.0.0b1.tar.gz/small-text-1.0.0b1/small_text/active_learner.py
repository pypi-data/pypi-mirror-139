import numpy as np

from abc import ABC, abstractmethod
from pathlib import Path

from scipy.sparse import csr_matrix

from small_text.base import LABEL_IGNORED
from small_text.exceptions import LearnerNotInitializedException
from small_text.utils.data import list_length
from small_text.utils.labels import concatenate
from small_text.utils.labels import get_ignored_labels_mask
from small_text.utils.labels import remove_by_index
from small_text.version import __version__ as version


class ActiveLearner(ABC):
    """Abstract base class for Active Learners."""

    @abstractmethod
    def query(self, num_samples=10):
        pass

    @abstractmethod
    def update(self, y):
        pass


class AbstractPoolBasedActiveLearner(ActiveLearner):

    def query(self, num_samples=10):
        pass

    def update(self, y):
        pass

    @abstractmethod
    def initialize_data(self, x_indices_initial, y_initial, *args, **kwargs):
        """(Re-)Initializes the current labeled pool.

        This methods needs to be called whenever the underlying data changes, in particularly
        before the first loop.

        Parameters
        ----------
        x_indices_initial : np.ndarray
            Positional indices pointing at training examples. This is the intially labelled set
            for training an initial classifier.
        y_initial : numpy.ndarray or scipy.sparse.csr_matrix
            The respective labels belonging to the examples referenced by `x_indices_initial`.
        """
        pass

    @property
    @abstractmethod
    def classifier(self):
        pass

    @property
    @abstractmethod
    def query_strategy(self):
        pass


class PoolBasedActiveLearner(AbstractPoolBasedActiveLearner):
    """A pool-based active learner in which a pool holds all available unlabeled data.

    It uses a classifier, a query strategy and manages the mutually exclusive partition over the
    whole training data into labeled and unlabeled.

    Parameters
    ----------
    clf_factory : small_text.classifiers.factories.AbstractClassifierFactory
        A factory responsible for creating new classifier instances.
    query_strategy : small_text.query_strategies.QueryStrategy
        Query strategy which is responsible for selecting instances during a `query()` call.
    x_train : ~small_text.data.datasets.Dataset
        A training dataset that is supported by the underlying classifier.
    reuse_model : bool, default=False
        Reuses the previous model during retraining (if a previous model exists),
        otherwise creates a new model for each retraining.

    Attributes
    ----------
    x_indices_labeled : numpy.ndarray
        Indices of instances (relative to `self.x_train`) constituting the labeled pool.
    x_indices_ignored : numpy.ndarray or scipy.sparse.csr_matrix
        Indices of instances (relative to `self.x_train`) which have been ignored,
        i.e. which will never be returned by a query.
    y : numpy.ndarray or scipy.sparse.csr_matrix
        Labels for the the current labeled pool. Each tuple `(x_indices_labeled[i], y[i])`
        represents one labeled sample.
    queried_indices : numpy.ndarray or None
        Queried indices returned by the last `query()` call, or `None` if no query has been
        executed yet.
    """

    def __init__(self, clf_factory, query_strategy, x_train, reuse_model=False):
        self._clf = None
        self._clf_factory = clf_factory
        self._query_strategy = query_strategy

        self._x_index_to_position = None

        self.x_train = x_train
        self.reuse_model = reuse_model

        self.x_indices_labeled = np.empty(shape=0, dtype=int)
        self.x_indices_ignored = np.empty(shape=0, dtype=int)

        self.y = None
        self.queried_indices = None

    def initialize_data(self, x_indices_initial, y_initial, x_indices_ignored=None,
                        x_indices_validation=None, retrain=True):
        """(Re-)Initializes the current labeled pool.

        This is required once before the first `query()` call, and whenever the labeled pool
        is changed from the outside, i.e. when `self.x_train` changes.

        Parameters
        ----------
        x_indices_initial : numpy.ndarray
            A list of indices (relative to `self.x_train`) of initially labeled samples.
        y_initial : numpy.ndarray or or scipy.sparse.csr_matrix
            Label matrix. One row corresponds to an index in `x_indices_initial`. If the
            passed type is numpy.ndarray (dense) all further label-based operations assume dense
            labels, otherwise sparse labels for scipy.sparse.csr_matrix.
        x_indices_ignored : numpy.ndarray
            List of ignored samples which will be invisible to the query strategy.
        x_indices_validation : numpy.ndarray
            The given indices (relative to `self.x_indices_labeled`) define a custom validation set
            if provided. Otherwise each classifier that uses a validation set will be responsible
            for creating a validation set. Only used if `retrain=True`.
        retrain : bool
            Retrains the model after the update if True.
        """
        self.x_indices_labeled = x_indices_initial
        self._x_index_to_position = self._build_x_index_to_position_index()
        self.y = y_initial

        if isinstance(self.y, csr_matrix):
            self.multi_label = True
        else:
            self.multi_label = False

        if x_indices_ignored is not None:
            self.x_indices_ignored = x_indices_ignored
        else:
            self.x_indices_ignored = np.empty(shape=(0), dtype=int)

        if retrain:
            self._retrain(x_indices_validation=x_indices_validation)

    def query(self, num_samples=10, x=None, query_strategy_kwargs=None):
        """Performs a query step, which selects a number of samples from the unlabeled pool.
        A query step must be followed by an update step.

        Parameters
        ----------
        num_samples : int
            Number of samples to query.
        x : list-like
            Alternative representation for the samples in the unlabeled pool.
            This is used by some query strategies.

        Returns
        -------
        queried_indices : numpy.ndarray
            List of queried indices (relative to the current unlabeled pool).

        Raises
        ------
        LearnerNotInitializedException
            Thrown when the active learner was not initialized via `initialize_data(...)`.
        ValueError
            Thrown when args or kwargs are not used and consumed.
        """
        if self._x_index_to_position is None:
            raise LearnerNotInitializedException()

        size = list_length(self.x_train)
        if x is not None and size != list_length(x):
            raise ValueError('Number of rows of alternative representation x must match the train '
                             'set (dim 0).')

        self.mask = np.ones(size, bool)
        self.mask[np.concatenate([self.x_indices_labeled, self.x_indices_ignored])] = False
        indices = np.arange(size)

        x = self.x_train if x is None else x
        query_strategy_kwargs = dict() if query_strategy_kwargs is None else query_strategy_kwargs
        self.queried_indices = self.query_strategy.query(self._clf,
                                                         x,
                                                         indices[self.mask],
                                                         self.x_indices_labeled,
                                                         self.y,
                                                         n=num_samples,
                                                         **query_strategy_kwargs)
        return self.queried_indices

    def update(self, y, x_indices_validation=None):
        """Performs an update step, which passes the label for each of the
        previously queried indices.

        An update step must be preceded by a query step. At the end of the update step the
        current model is retrained using all available labels.

        Parameters
        ----------
        y : numpy.ndarray or scipy.sparse.csr_matrix
            Labels provided in response to the previous query. Each label at index i corresponds
            to the sample x[i] for single-label data (ndarray) and each row of labels at index i
            corresponds to the sample x[i] for multi-label data (csr_matrix). Setting the label /
            row of labels to ` small_text.base import LABEL_IGNORED` will ignore the respective
            sample.
        x_indices_validation : numpy.ndarray
            The given indices (relative to `self.x_indices_labeled`) define a custom validation set
            if provided. Otherwise each classifier that uses a validation set will be responsible
            for creating a validation set.
        """
        if self.queried_indices.shape[0] != y.shape[0]:
            raise ValueError('Query-update mismatch: indices queried - {} / labels provided - {}'
                             .format(self.queried_indices.shape[0], y.shape[0])
                             )

        ignored = get_ignored_labels_mask(y, LABEL_IGNORED)
        if ignored.any():
            y = remove_by_index(y, np.arange(y.shape[0])[ignored])
            self.x_indices_ignored = np.concatenate([self.x_indices_ignored, self.queried_indices[ignored]])

        self.x_indices_labeled = np.concatenate([self.x_indices_labeled, self.queried_indices[~ignored]])
        self._x_index_to_position = self._build_x_index_to_position_index()

        if self.x_indices_labeled.shape[0] != np.unique(self.x_indices_labeled).shape[0]:
            raise ValueError('Duplicate indices detected in the labeled pool! '
                             'Please re-examine your query strategy.')

        if not ignored.all():
            self.y = concatenate(self.y, y)
            self._retrain(x_indices_validation=x_indices_validation)

        self.queried_indices = None
        self.mask = None

    def update_label_at(self, x_index, y, retrain=False, x_indices_validation=None):
        """Updates the label for the given x_index (with regard to `self.x_train`).

        Notes
        -----
        After adding labels the current model might not reflect the labeled data anymore.
        You should consider if a retraining is necessary when using this operation.
        Since retraining is often time-consuming, `retrain` is set to `False` by default.

        Parameters
        ----------
        x_index : int
            Data index (relative to `self.x_train`) for which the label should be updated.
        y : int or numpy.ndarray
            The new label(s) to be assigned for the sample at `self.x_indices_labeled[x_index]`.
        retrain : bool
            Retrains the model after the update if True.
        x_indices_validation : numpy.ndarray
            The given indices (relative to `self.x_indices_labeled`) define a custom validation set
            if provided. This is only used if `retrain` is `True`.
        """
        position = self._x_index_to_position[x_index]
        self.y[position] = y

        if retrain:
            self._retrain(x_indices_validation=x_indices_validation)

    def remove_label_at(self, x_index, retrain=False, x_indices_validation=None):
        """Removes the labeling for the given x_index (with regard to `self.x_train`).

        Notes
        -----
        After removing labels the current model might not reflect the labeled data anymore.
        You should consider if a retraining is necessary when using this operation.
        Since retraining is often time-consuming, `retrain` is set to `False` by default.

        Parameters
        ----------
        x_index : int
            Data index (relative to `self.x_train`) for which the label should be removed.
        retrain : bool
            Retrains the model after removal if True.
        x_indices_validation : numpy.ndarray
            The given indices (relative to `self.x_indices_labeled`) define a custom validation set
            if provided. This is only used if `retrain` is `True`.
        """

        position = self._x_index_to_position[x_index]
        self.y = remove_by_index(self.y, position)
        self.x_indices_labeled = np.delete(self.x_indices_labeled, position)

        if retrain:
            self._retrain(x_indices_validation=x_indices_validation)

    def ignore_sample_at(self, x_index, retrain=False, x_indices_validation=None):
        """Ignores the sample at the given `x_index.

        Any labels which had previously been assigned to this sample will be removed.

        Notes
        -----
        If ignoring a sample incurs the removal of a label label, the current model might not
        reflect the labeled data anymore. You should consider if a retraining is necessary when
        using this operation. Since retraining is often time-consuming, `retrain` is set to
        `False` by default.

        Parameters
        ----------
        x_index : int
           Data index (relative to `self.x_train`) for which the label should be ignored.
        retrain : bool
            Retrains the model after the removal if True.
        x_indices_validation : numpy.ndarray
            The given indices (relative to `self.x_indices_labeled`) define a custom validation set
            if provided. This is only used if `retrain` is `True`.
        """

        labeling_exists = x_index in self._x_index_to_position
        if labeling_exists:
            position = self._x_index_to_position[x_index]
            self.y = remove_by_index(self.y, position)
            self.x_indices_labeled = np.delete(self.x_indices_labeled, position)

        self.x_indices_ignored = np.concatenate([self.x_indices_ignored, [x_index]])

        if labeling_exists and retrain:
            self._retrain(x_indices_validation=x_indices_validation)

    def save(self, file):
        """Serializes the current active learner object into a single file for later re-use.

        Parameters
        ----------
        file : str or path or file
            Serialized output file to be written.
        """
        if isinstance(file, (str, Path)):
            with open(file, 'wb+') as f:
                self._save(f)
        else:
            self._save(file)

    def _save(self, file_handle):
        import dill as pickle
        pickle.dump(version, file_handle)
        pickle.dump(self, file_handle)

    @classmethod
    def load(cls, file):
        """Deserializes a serialized active learner.

        Parameters
        ----------
        file : str or path or file
            File to be loaded.
        """
        if isinstance(file, (str, Path)):
            with open(file, 'rb') as f:
                return cls._load(f)
        else:
            return cls._load(file)

    @classmethod
    def _load(cls, file_handle):
        import dill as pickle
        _ = pickle.load(file_handle)  # version, will be used in the future
        return pickle.load(file_handle)

    @property
    def classifier(self):
        return self._clf

    @property
    def query_strategy(self):
        return self._query_strategy

    def _retrain(self, x_indices_validation=None):
        if self._clf is None or not self.reuse_model:
            if hasattr(self, '_clf'):
                del self._clf
            self._clf = self._clf_factory.new()

        x = self.x_train[self.x_indices_labeled]

        if x_indices_validation is None:
            self._clf.fit(x)
        else:
            indices = np.arange(self.x_indices_labeled.shape[0])
            mask = np.isin(indices, x_indices_validation)

            x_train = x[indices[~mask]]
            x_valid = x[indices[mask]]

            self._clf.fit(x_train, validation_set=x_valid)

    def _build_x_index_to_position_index(self):
        return dict({
            x_index: position for position, x_index in enumerate(self.x_indices_labeled)
        })
