import os
import json
import argparse
import time
import logging

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from preprocessing.embeddings import embed
from preprocessing.utils import LocalTextCategorizationDataset


logger = logging.getLogger(__name__)


def train(model_path, dataset_path, params):

    artefacts_path = os.path.join(model_path, time.strftime('%Y-%m-%d-%H-%M-%S'))

    dataset = LocalTextCategorizationDataset(
        dataset_path,
        batch_size=params['batch_size'],
        min_samples_per_label=params['min_samples_per_label'],
        preprocess_text=embed)

    logger.info(dataset)

    model = Sequential()
    model.add(Dense(params['dense_dim'], activation='relu'))
    model.add(Dense(dataset.get_num_labels(), activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

    train_history = model.fit(
        dataset.get_train_sequence(),
        validation_data=dataset.get_test_sequence(),
        epochs=params['epochs'],
        verbose=params['verbose'],
        workers=params['workers'],
        use_multiprocessing=params['use_multiprocessing']
    )

    scores = model.evaluate_generator(dataset.get_test_sequence(), verbose=0)
    logger.info("Test Accuracy: {:.2f}".format(scores[1] * 100))

    os.makedirs(artefacts_path, exist_ok=True)

    model.save(os.path.join(artefacts_path, "model.h5"))

    with open(os.path.join(artefacts_path, "params.json"), "w") as f:
        json.dump(params, f)

    with open(os.path.join(artefacts_path, 'labels_index.json'), 'w') as f:
        json.dump(dataset.get_label_to_index_map(), f)

    # train_history.history is not JSON-serializable because it contains numpy arrays
    serializable_hist = {k: [float(e) for e in v] for k, v in train_history.history.items()}
    with open(os.path.join(artefacts_path, "train_output.json"), "w") as f:
        json.dump(serializable_hist, f)

    return scores[1]


if __name__ == "__main__":
    import yaml

    parser = argparse.ArgumentParser()

    parser.add_argument("artefacts_path", help="Folder where training artefacts will be persisted")
    parser.add_argument("dataset_path", help="Path to training dataset")
    parser.add_argument("config_path", help="Path to Yaml file specifying training parameters")
    args = parser.parse_args()

    with open(args.config_path, 'r') as config_f:
        params = yaml.safe_load(config_f.read())

    logger.info(f"Training model with parameters: {params}")

    train(args.artefacts_path, args.dataset_path, params)

