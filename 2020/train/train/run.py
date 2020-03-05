import os
import json
import argparse
import time
import logging
import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from preprocessing.embeddings import embed
from preprocessing.utils import LocalTextCategorizationDataset
from preprocessing.utils_production import LocalLargeTextCategorizationDataset


logger = logging.getLogger(__name__)


def train(model_path, dataset_path, train_params, add_timestamp):

    if add_timestamp:
        artefacts_path = os.path.join(model_path, time.strftime('%Y-%m-%d-%H-%M-%S'))
    else:
        artefacts_path = model_path

    dataset = LocalTextCategorizationDataset(
        dataset_path,
        batch_size=train_params['batch_size'],
        min_samples_per_label=train_params['min_samples_per_label'],
        preprocess_text=embed)

    logger.info(dataset)

    model = Sequential()
    model.add(Dense(train_params['dense_dim'], activation='relu', input_shape=(768, )))
    model.add(Dense(dataset.get_num_labels(), activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

    train_history = model.fit(
        dataset.get_train_sequence(),
        validation_data=dataset.get_test_sequence(),
        epochs=train_params['epochs'],
        verbose=train_params['verbose'],
        workers=train_params['workers'],
        use_multiprocessing=train_params['use_multiprocessing']
    )

    scores = model.evaluate_generator(dataset.get_test_sequence(), verbose=0)
    logger.info("Test Accuracy: {:.2f}".format(scores[1] * 100))

    os.makedirs(artefacts_path, exist_ok=True)

    model.save(os.path.join(artefacts_path, "model.h5"))

    with open(os.path.join(artefacts_path, "params.json"), "w") as f:
        json.dump(train_params, f)

    with open(os.path.join(artefacts_path, 'labels_index.json'), 'w') as f:
        json.dump(dataset.get_label_to_index_map(), f)

    # train_history.history is not JSON-serializable because it contains numpy arrays
    serializable_hist = {k: [float(e) for e in v] for k, v in train_history.history.items()}
    with open(os.path.join(artefacts_path, "train_output.json"), "w") as f:
        json.dump(serializable_hist, f)

    return scores[1], artefacts_path


def train_production(model_path, train_dataset_paths, test_dataset_paths,
                     labels_path, train_params):
    limit_train = train_params['limit'] if 'limit' in train_params else None
    limit_test = .3 * limit_train / .7 if limit_train else None

    train_dataset = LocalLargeTextCategorizationDataset(
        train_dataset_paths,
        labels_path,
        batch_size=train_params['batch_size'],
        preprocess_text=embed,
        limit=limit_train)

    test_dataset = LocalLargeTextCategorizationDataset(
        test_dataset_paths,
        labels_path,
        batch_size=train_params['batch_size'],
        preprocess_text=embed,
        limit=limit_test)

    model = Sequential()
    model.add(Dense(train_params['dense_dim'], activation='relu'))
    model.add(Dense(len(train_dataset.label_list), activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

    train_history = model.fit(
        train_dataset.get_sequence(),
        validation_data=test_dataset.get_sequence(),
        epochs=train_params['epochs'],
        verbose=train_params['verbose'],
        workers=train_params['workers'],
        use_multiprocessing=train_params['use_multiprocessing']
    )

    scores = model.evaluate(test_dataset.get_sequence(), verbose=0)
    logger.info("Test Accuracy: {:.2f}".format(scores[1] * 100))

    os.makedirs(model_path, exist_ok=True)

    model.save(os.path.join(model_path, "model.h5"))

    with open(os.path.join(model_path, "params.json"), "w") as f:
        json.dump(train_params, f)

    # train_history.history is not JSON-serializable because it contains numpy arrays
    serializable_hist = {k: [float(e) for e in v] for k, v in train_history.history.items()}
    with open(os.path.join(model_path, "train_output.json"), "w") as f:
        json.dump(serializable_hist, f)


if __name__ == "__main__":
    import yaml

    parser = argparse.ArgumentParser()

    parser.add_argument("artefacts_path", help="Folder where training artefacts will be persisted")
    parser.add_argument("dataset_path", help="Path to training dataset")
    parser.add_argument("config_path", help="Path to Yaml file specifying training parameters")
    parser.add_argument("--add_timestamp", action='store_true',
                        help="Create artefacts in a subfolder with name equal to execution timestamp")

    args = parser.parse_args()

    with open(args.config_path, 'r') as config_f:
        train_params = yaml.safe_load(config_f.read())

    logger.info(f"Training model with parameters: {train_params}")

    train(args.artefacts_path, args.dataset_path, train_params, args.add_timestamp)
