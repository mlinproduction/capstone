import numpy as np
import pandas as pd

from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import to_categorical

from sklearn.model_selection import train_test_split


def integer_floor(float_value: float):
    return int(np.floor(float_value))


class _SimpleSequence(Sequence):
    def __init__(self, get_batch_method, num_batches_method):
        self.get_batch_method = get_batch_method
        self.num_batches_method = num_batches_method

    def __len__(self):
        return self.num_batches_method()

    def __getitem__(self, idx):
        return self.get_batch_method()


class BaseTextCategorizationDataset:
    def __init__(self, batch_size, train_ratio=0.8):
        assert train_ratio < 1.0
        self.train_ratio = train_ratio
        self.batch_size = batch_size

    def _get_label_list(self):
        raise NotImplementedError

    def get_num_labels(self):
        return len(self._get_label_list())

    def _get_num_samples(self):
        raise NotImplementedError

    def _get_num_train_samples(self):
        return integer_floor(self.train_ratio * self._get_num_samples())

    def _get_num_test_samples(self):
        return self._get_num_samples() - self._get_num_train_samples()

    def _get_num_train_batches(self):
        return integer_floor(self._get_num_train_samples() / self.batch_size)

    def _get_num_test_batches(self):
        return integer_floor(self._get_num_test_samples() / self.batch_size)

    def get_train_batch(self):
        raise NotImplementedError

    def get_test_batch(self):
        raise NotImplementedError

    def get_index_to_label_map(self):
        label_list = self._get_label_list()
        return {i: label for i, label in enumerate(label_list)}

    def get_label_to_index_map(self):
        return {v: k for k, v in self.get_index_to_label_map().items()}

    def to_indexes(self, labels):
        label_to_index= self.get_label_to_index_map()
        return [label_to_index[l] for l in labels]

    def get_train_sequence(self):
        return _SimpleSequence(self.get_train_batch, self._get_num_train_batches)

    def get_test_sequence(self):
        return _SimpleSequence(self.get_test_batch, self._get_num_test_batches)

    def __repr__(self):
        return self.__class__.__name__ + \
               f"(n_train_samples: {self._get_num_train_samples()}, " \
               f"n_test_samples: {self._get_num_test_samples()}, " \
               f"n_labels: {self.get_num_labels()})"


class LocalTextCategorizationDataset(BaseTextCategorizationDataset):
    """
    A TextCategorizationDataset read from a file residing in the local filesystem
    """
    def __init__(self, filename, batch_size,  multilabel=False,
                 train_ratio=0.8, min_samples_per_label=100, preprocess_text=lambda x: x):
        """
        :param filename: a CSV file containing the text samples in the format
            (post_id 	tag_name 	tag_id 	tag_position 	title)
        :param batch_size: number of samples per batch
        :param multilabel: bool, whether we want the dataset as a multilabel (True) or single label (False)
        :param train_ratio: ratio of samples dedicated to training set between (0, 1)
        :param preprocess_text: function taking an array of text and returning a numpy array, default identity
        """
        super().__init__(batch_size, train_ratio)
        self.filename = filename
        self.multilabel = multilabel
        self.preprocess_text = preprocess_text

        if self.multilabel:
            raise NotImplementedError
        else:
            self._dataset = self.load_dataset(filename, min_samples_per_label)

            assert self._get_num_train_batches() > 0
            assert self._get_num_test_batches() > 0

            self._label_list = self._dataset['tag_name']\
                .value_counts()\
                .index.values

            y = self.to_indexes(self._dataset['tag_name'])
            y = to_categorical(y, num_classes=len(self._label_list))

            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
                self._dataset['title'],
                y,
                train_size=self._get_num_train_samples(),
                stratify=y)

            self.train_batch_index = 0
            self.test_batch_index = 0

    @staticmethod
    def load_dataset(filename, min_samples_per_label):
        _dataset = pd.read_csv(filename)

        assert all(c in _dataset.columns for c in
                   {'post_id', 'tag_name', 'tag_id', 'tag_position', 'title'})

        def filter_tag_position(position):
            def filter_function(df):
                return df.loc[df.tag_position == position]

            return filter_function

        def filter_tags_with_less_than_x_samples(x):
            def filter_function(df):
                tag_counts = df.groupby('tag_name')['post_id'].nunique()
                tags_with_at_least_10 = tag_counts[tag_counts >= x].index.values
                return df.loc[df.tag_name.isin(tags_with_at_least_10)]

            return filter_function

        return _dataset.pipe(filter_tag_position(0)) \
            .pipe(filter_tags_with_less_than_x_samples(min_samples_per_label))

    def _get_label_list(self):
        return self._label_list

    def _get_num_samples(self):
        return self._dataset.shape[0]

    def get_train_batch(self):
        i = self.train_batch_index
        next_x = self.preprocess_text(self.x_train[(i * self.batch_size):((i + 1) * self.batch_size)])
        next_y = self.y_train[(i * self.batch_size):((i + 1) * self.batch_size)]
        # When we reach the max num batches, we start anew
        self.train_batch_index = (self.train_batch_index  + 1) % self._get_num_train_batches()
        return next_x, next_y

    def get_test_batch(self):
        i = self.test_batch_index
        next_x = self.preprocess_text(self.x_test[(i * self.batch_size):((i + 1) * self.batch_size)])
        next_y = self.y_test[(i * self.batch_size):((i + 1) * self.batch_size)]
        # When we reach the max num batches, we start anew
        self.test_batch_index = (self.test_batch_index + 1) % self._get_num_test_batches()
        return next_x, next_y

