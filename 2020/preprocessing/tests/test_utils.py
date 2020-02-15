import unittest
from unittest.mock import patch
import pandas as pd

from preprocessing import utils

@patch("preprocessing.utils.BaseTextCategorizationDataset._get_label_list")
@patch("preprocessing.utils.BaseTextCategorizationDataset._get_num_samples")
class TestBaseTextCategorizationDataset(unittest.TestCase):
    def test__get_num_train_samples(self, mocked_get_num_samples, mocked_get_label_list):
        mocked_get_num_samples.return_value = 100
        base = utils.BaseTextCategorizationDataset(20, 0.8)
        self.assertEqual(base._get_num_train_samples(), 80)

    def test__get_num_train_batches(self, mocked_get_num_samples, mocked_get_label_list):
        mocked_get_num_samples.return_value = 100
        base = utils.BaseTextCategorizationDataset(20, 0.8)
        self.assertEqual(base._get_num_train_batches(), 4)

    def test__get_num_test_batches(self, mocked_get_num_samples, mocked_get_label_list):
        mocked_get_num_samples.return_value = 100
        base = utils.BaseTextCategorizationDataset(20, 0.8)
        self.assertEqual(base._get_num_test_batches(), 1)

    def test_get_index_to_label_map(self, mocked_get_num_samples, mocked_get_label_list):
        mocked_get_label_list.return_value = ['a', 'b', 'c']
        base = utils.BaseTextCategorizationDataset(20, 0.8)
        self.assertEqual(base.get_index_to_label_map(), {0: 'a', 1: 'b', 2: 'c'})

    def test_index_to_label_and_label_to_index_are_identity(self, mocked_get_num_samples, mocked_get_label_list):
        mocked_get_label_list.return_value = ['a', 'b', 'c']
        base = utils.BaseTextCategorizationDataset(20, 0.8)
        label_to_index = base.get_label_to_index_map()
        for i, label in base.get_index_to_label_map().items():
            self.assertEqual(i, label_to_index[label])

    def test_to_indexes(self, mocked_get_num_samples, mocked_get_label_list):
        mocked_get_label_list.return_value = ['a', 'b', 'c']
        base = utils.BaseTextCategorizationDataset(20, 0.8)
        self.assertEqual(base.to_indexes(mocked_get_label_list.return_value), [0, 1, 2])

@patch("pandas.read_csv")
class TestLocalTextCategorizationDataset(unittest.TestCase):
    def test_load_dataset_returns_expected_data(self, read_csv_mock):
        read_csv_mock.return_value = pd.DataFrame({
            'post_id': ['id_1', 'id_2'],
            'tag_name': ['tag_a', 'tag_b'],
            'tag_id': [1, 2],
            'tag_position': [0, 1],
            'title': ['title_1', 'title_2']
        })
        dataset = utils.LocalTextCategorizationDataset.load_dataset('fake.csv', 1)
        self.assertEqual(dataset.loc[dataset['tag_position'] > 0].shape[0], 0)
        self.assertEqual(dataset.loc[dataset['tag_position'] == 0].shape[0], 1)

    def test__get_num_samples_is_correct(self, read_csv_mock):
        read_csv_mock.return_value = pd.DataFrame({
            'post_id': ['id_1', 'id_2', 'id_3'],
            'tag_name': ['tag_a', 'tag_a', 'tag_a'],
            'tag_id': [1, 1, 1],
            'tag_position': [0, 0, 0],
            'title': ['title_1', 'title_2', 'title_3']
        })
        dataset = utils.LocalTextCategorizationDataset(
            'fake.csv', 1, train_ratio=0.5, min_samples_per_label=1)
        self.assertEqual(dataset._get_num_samples(), 3)

    def test_get_train_batch_returns_expected_shape(self, read_csv_mock):
        read_csv_mock.return_value = pd.DataFrame({
            'post_id': ['id_1', 'id_2', 'id_3'],
            'tag_name': ['tag_a', 'tag_a', 'tag_a'],
            'tag_id': [1, 1, 1],
            'tag_position': [0, 0, 0],
            'title': ['title_1', 'title_2', 'title_3']
        })
        dataset = utils.LocalTextCategorizationDataset(
            'fake.csv', 1, train_ratio=0.5, min_samples_per_label=1)
        x_batch, y_batch = dataset.get_train_batch()
        self.assertEqual(x_batch.shape, (1,))
        self.assertEqual(y_batch.shape, (1, 1))

    def test_get_test_batch_returns_expected_shape(self, read_csv_mock):
        read_csv_mock.return_value = pd.DataFrame({
            'post_id': ['id_1', 'id_2', 'id_3'],
            'tag_name': ['tag_a', 'tag_a', 'tag_a'],
            'tag_id': [1, 1, 1],
            'tag_position': [0, 0, 0],
            'title': ['title_1', 'title_2', 'title_3']
        })
        dataset = utils.LocalTextCategorizationDataset(
            'fake.csv', 1, train_ratio=0.5, min_samples_per_label=1)
        x_batch, y_batch = dataset.get_test_batch()
        self.assertEqual(x_batch.shape, (1,))
        self.assertEqual(y_batch.shape, (1, 1))

    def test_get_train_batch_raises_assertion_error(self, read_csv_mock):
        read_csv_mock.return_value = pd.DataFrame({
            'post_id': ['id_1', 'id_2', 'id_3'],
            'tag_name': ['tag_a', 'tag_a', 'tag_a'],
            'tag_id': [1, 1, 1],
            'tag_position': [0, 0, 0],
            'title': ['title_1', 'title_2', 'title_3']
        })
        dataset = utils.LocalTextCategorizationDataset(
            'fake.csv', 1, train_ratio=0.5, min_samples_per_label=1)
        dataset.get_test_batch()
        dataset.get_test_batch()
        # there should only be 2 batches, an assertion error should be rised at the 3rd
        with self.assertRaises(AssertionError):
            dataset.get_test_batch()

    def test_get_train_batch_raises_assertion_error(self, read_csv_mock):
        read_csv_mock.return_value = pd.DataFrame({
            'post_id': ['id_1', 'id_2', 'id_3'],
            'tag_name': ['tag_a', 'tag_a', 'tag_a'],
            'tag_id': [1, 1, 1],
            'tag_position': [0, 0, 0],
            'title': ['title_1', 'title_2', 'title_3']
        })
        dataset = utils.LocalTextCategorizationDataset(
            'fake.csv', 1, train_ratio=0.5, min_samples_per_label=1)
        dataset.get_test_batch()
        with self.assertRaises(AssertionError):
            dataset.get_test_batch()