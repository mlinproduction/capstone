import pandas as pd
from tensorflow.keras.utils import to_categorical


class LocalLargeTextCategorizationDataset(object):
    def __init__(self, dataset_paths, labels_path, batch_size, preprocess_text):
        self.dataset_paths = dataset_paths
        self.batch_size = batch_size
        self.preprocess_text = preprocess_text
        self.labels_path = labels_path
        self._label_list = None

    @property
    def label_list(self):
        if not(self._label_list):
            self._label_list = pd.read_csv(self.labels_path)['tag_name']

        return self._label_list

    def get_index_to_label_map(self):
        label_list = self.label_list
        return {i: label for i, label in enumerate(label_list)}

    def get_label_to_index_map(self):
        return {v: k for k, v in self.get_index_to_label_map().items()}

    def to_indexes(self, labels):
        label_to_index = self.get_label_to_index_map()
        return [label_to_index[l] for l in labels]

    def get_sequence(self):
        for path in self.dataset_paths:
            current_df = pd.read_csv(path, chunksize=self.batch_size)
            for batch_df in current_df:
                y = self.to_indexes(batch_df['tag_name'])
                y = to_categorical(y, num_classes=len(self._label_list))
                yield (self.preprocess_text(batch_df['title']), y)
