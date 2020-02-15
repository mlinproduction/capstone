# ML In Prod 2020 Capstone

## Requirements


## Setup


## Training a model


1. Setup the training parameters, by copying `conf/train-conf.yml.dist` into `conf/train-conf.yml` and editing the
parameters to your taste

2. Download the data

3. Run the training job using the commands:
```bash
conda activate ml_in_prod_capstone
python train/run.py data/artefacts ${dataset_filename} conf/train-conf.yml
```
where you will need to replace `${dataset_filename}` by the location of the dataset you want to train on.

4. The script will generate the artefacts in a folder within `data/artefacts` with name equal to a timestamp. You can now
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

musts:
-1: revert env variable change: x
0- move project to github repo: x
0.5 - make datafile available from google cloud and have makefile command to download it:
1- conda env setup (global for all modules)
2- make predict tests work
3- Fix Dockerfile and make it work for train & inference
4- Write documentation in README's
5- figure out how to include internal dependencies in setup.py


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