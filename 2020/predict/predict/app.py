import json
import argparse
import logging
import time
import os

logger = logging.getLogger(__name__)

from flask import Flask, request

from run import TextPredictionModel

parser = argparse.ArgumentParser()
parser.add_argument("--artefacts_path", type=str, help="path to trained model artefacts")
parser.add_argument("--port", type=int, default=5000, help="port")
args = parser.parse_args()

if args.artefacts_path is None:
    if os.getenv('ARTEFACTS_PATH') is not None:
        args.artefacts_path = os.getenv('ARTEFACTS_PATH')
    else:
        raise ValueError(
            "Please provide the `artefacts_path` as a command line argument or"
            " as an environment variable `ARTEFACTS_PATH`")

app = Flask(__name__)

logger.info(f"Loading model from: `{args.artefacts_path}`")

model = TextPredictionModel.from_artefacts(args.artefacts_path)
created_at = time.strftime('%Y-%m-%d-%H-%M-%S')


@app.route("/tag/predict/", methods=["POST"])
def predict_tag():

    text = request.form.get("text")
    logger.info(f"Predict tag for text=`{text}`")
    prediction = model.predict([text])
    logger.info(f"Predictions: {prediction}")

    return app.response_class(
        response=json.dumps(prediction),
        status=200,
        mimetype='application/json'
    )

@app.route("/tag/status/")
def status():
    status = {
        'model': {
            'params': model.params,
            'labels_to_index': model.labels_to_index,
            'artefacts_path': args.artefacts_path
        },
        'created_at': created_at
    }
    return app.response_class(
        response=json.dumps(status),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    stream_handler = logging.StreamHandler(stream=None)
    file_handler = logging.FileHandler('app.log')

    logging.basicConfig(format="%(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO,
                        handlers=[stream_handler, file_handler])

    app.run(debug=True, host="0.0.0.0", port=args.port)
