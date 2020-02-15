import unittest

from predict.run import TextPredictionModel

class TextPredictionModelTest(unittest.TestCase):

    def test_predict():
        pass

        #TODO: Fix this:
        model = TextPredictionModel()
        text = 'ruby on rails: how to change BG color of options in select list, ruby-on-rails'
        prediction = predict([text], model_path="../train/train/tests/models/")

        assert prediction[0] == 'ruby-on-rails'

