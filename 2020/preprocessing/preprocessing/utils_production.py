import pandas as pd


class LocalLargeTextCategorizationDataset(object):
    def __init__(self, dataset_paths, batch_size, preprocess_text):
        self.dataset_paths = dataset_paths
        self.batch_size = batch_size
        self.preprocess_text = preprocess_text

    def get_sequence(self):
        for path in self.dataset_paths:
            current_df = pd.read_csv(path, chunksize=self.batch_size)
            for batch in current_df:
                yield batch
