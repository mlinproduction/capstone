import unittest
import tempfile
from unittest.mock import patch
from predict.run import TextPredictionModel
from train import run
import pandas as pd


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
    tags = [
        "php",
        "ruby-on-rails",
        "php",
        "ruby-on-rails",
        "php",
        "ruby-on-rails",
        "php",
        "ruby-on-rails",
        "php",
        "ruby-on-rails",
    ]

    return pd.DataFrame({"title": titles, "tag_name": tags})


class TextPredictionModelTest(unittest.TestCase):

    @patch(
        "preprocessing.utils.LocalTextCategorizationDataset.load_dataset",
        side_effect=load_dataset_mock,
    )
    def test_train(self, _):

        params = {
            "dense_dim": 64,
            "epochs": 10,
            "batch_size": 2,
            "min_samples_per_label": 10,
            "verbose": 1,
            "workers": 1,
            "use_multiprocessing": False,
        }

        with tempfile.TemporaryDirectory() as model_dir:
            _, artefacts_path = run.train(model_dir, "dummy_dataset_path", params)

            model = TextPredictionModel.from_artefacts(artefacts_path)
            text = 'ruby on rails: how to change BG color of options in select list, ruby-on-rails'
            prediction = model.predict([text])


            assert [x for x in prediction[0].items()][0][0] == 'ruby-on-rails'