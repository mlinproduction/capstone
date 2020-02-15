# ML In Prod 2020 Capstone

This repository contains the capstone project for the 2020 edition
of the [ML In Production course](https://mlinproduction.github.io/) taking place in February-March 2020 
in Barcelona, Spain.

## Requirements

Before proceeding, please make sure you have 

* conda (we recommend installing the [miniconda](https://docs.conda.io/en/latest/miniconda.html) version)
* curl
* GNU make

## Setup

The project uses conda environments. To set the project environment (named `ml_in_prod_capsone`), please run

```bash
make setup
```

## Training a model


1. Setup the training parameters, by copying `conf/train-conf.yml.dist` into `conf/train-conf.yml` and editing the
parameters to your taste

2. Run the training job using the commands:
```bash
make train
```
which will download the dataset and train the model. Optionally, you can also pass it the path to the dataset:
```bash
make train DATASET=/path/to/dataset
```
3. The script will generate the artefacts in a folder within `data/artefacts` with name equal to a timestamp. You can now
copy the path to this folder and use it to test or deploy the trained model, see section below.

## Deploying or testing a trained model

1. Copy the file `2020/predict/predict.conf.dist` into `2020/predict/predict.conf` and edit the fields to your taste
2. `make help` and choose one of the available targets, for instance
```bash
make predict-test TEXT="my text"
```

## Disclaimer

This is an educational project. To that end, we have taken a number of shortcuts that would not be appropriate for a production deployment, for instance:
- dockerfiles should be separate for train/inference
- embedding info should be serialized with model to ensure compatibility
- return proper responses with text/json content-type (https://tedboy.github.io/flask/quickstart/quickstart9.html)
- use proper WSGI instead of Flask's dev server (https://flask.palletsprojects.com/en/1.1.x/deploying/) 
- handle errors gracefully so that a proper response is returned instead of HTML with the stacktrace
- dev / prod environments usually are different and hence are managed through different Yamls
