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

The project environment uses conda environments. To set the project environment (named `ml_in_prod_capsone`), please run

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
where you will need to replace `${dataset_filename}` by the location of the dataset you want to train on.

3. The script will generate the artefacts in a folder within `data/artefacts` with name equal to a timestamp. You can now
copy the path to this folder and use it to test or deploy the trained model, see section below.

## Deploying or testing a trained model

1. Copy the file `2020/predict/predict.conf.dist` into `2020/predict/predict.conf` and edit the fields to your taste
2. Activate the conda environment (`conda activate ml_in_prod_capstone`)
3. `make help` and choose one of the available targets, for instance
```bash
conda activate ml_in_prod_capstone
make predict-test TEXT="my text"
```

## TODOS

nice to have:
1- Cache app endpoints to avoid recomputation for same input
2- Ser/Deser in same class
3- use JSON for POST so that we can pass several text inputs at once


Disclaimer:
- dockerfiles should be separate for train/inference
- embedding info should be serialized with model to ensure compatibility
- return proper responses with text/json content-type (https://tedboy.github.io/flask/quickstart/quickstart9.html)
- use proper WSGI instead of Flask's dev server (https://flask.palletsprojects.com/en/1.1.x/deploying/) 
- handle errors gracefully so that a proper response is returned instead of HTML with the stacktrace
- dev / prod environments usually are different and hence are managed through different Yamls