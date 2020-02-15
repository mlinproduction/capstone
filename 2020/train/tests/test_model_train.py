from unittest.mock import patch
import unittest
import tempfile

import pandas as pd

from train import run


def load_dataset_mock(filename, min_samples_per_label):
    titles = [
        "Is it possible to execute the procedure of a function in the scope of the caller?",
        "ruby on rails: how to change BG color of options in select list, ruby-on-rails",
        "Is it possible to execute the procedure of a function in the scope of the caller?",
        "ruby on rails: how to change BG color of options in select list, ruby-on-rails",
        "Is it possible to execute the procedure of a function in the scope of the caller?",
        "ruby on rails: how to change BG color of options in select list, ruby-on-rails",
        "Is it possible to execute the procedure of a function in the scope of the caller?",
        "ruby on rails: how to change BG color of options in select list, ruby-on-rails",
        "Is it possible to execute the procedure of a function in the scope of the caller?",
        "ruby on rails: how to change BG color of options in select list, ruby-on-rails",
    ]
    tags = ["php", "ruby-on-rails", "php", "ruby-on-rails", "php", "ruby-on-rails", "php", "ruby-on-rails",
            "php", "ruby-on-rails"]

    return pd.DataFrame({
        'title': titles,
        'tag_name': tags
    })


class TestTrain(unittest.TestCase):

    @patch("preprocessing.utils.LocalTextCategorizationDataset.load_dataset", side_effect=load_dataset_mock)
    def test_train(self, _):

        params = {"dense_dim": 64, "epochs": 10, "batch_size": 2}

        with tempfile.TemporaryDirectory() as model_dir:
            accuracy = run.train(model_dir, 'dummy_dataset_path', params)

        self.assertEqual(accuracy, 1.0)
