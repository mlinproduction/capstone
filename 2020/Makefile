# Good config practices, cf: https://tech.davis-hansson.com/p/make/
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

CONDA_ROOT = /$(shell which conda | cut -d "/" -f2)
PIP = $(CONDA_ROOT)/envs/ml_in_prod_capstone/bin/pip
NOSE = $(CONDA_ROOT)/envs/ml_in_prod_capstone/bin/nosetests
PYTHON = $(CONDA_ROOT)/envs/ml_in_prod_capstone/bin/python

# *******************************************************************************************************************
# Setup
# *******************************************************************************************************************

.setup_done: environment.yml
	echo "Using conda at $(CONDA_ROOT)"
	conda env create --force -f environment.yml
	$(PIP) install -e preprocessing/
	$(PIP) install -e train/
	$(PIP) install -e predict/
	$(NOSE) -v preprocessing/tests
	$(NOSE) -v train/tests
	$(NOSE) -v predict/tests

.PHONY: setup
setup: .setup_done ## Creates project environment, installs packages and runs tests

# *******************************************************************************************************************
# Training
# *******************************************************************************************************************

DATASET_DEFAULT=train/data/stackoverflow_posts.csv
DATASET ?= $(DATASET_DEFAULT)

$(DATASET_DEFAULT):
	curl -L -o $(DATASET_DEFAULT) "https://docs.google.com/uc?export=download&id=1ud6JR2JjkRi-iRrsx8kWj4rPL5BVt5Pd"

.PHONY: download ## Downloads the data to train the model
download: $(DATASET_DEFAULT)

.training_done: $(DATASET) .setup_done
	python train/run.py data/artefacts ${dataset_filename} conf/train-conf.yml

.PHONY: train
train: .training_done ## Trains a model

# *******************************************************************************************************************
# Prediction / deployment targets
# *******************************************************************************************************************

include predict/predict.conf

TEXT ?= $(TEST_TEXT)

predict-test: .setup_done ## Calling predict from terminal
	$(PYTHON) predict/predict/run.py $(ARTEFACTS_PATH) --text="$(TEXT)"

flask-server-local: .setup_done ## Starts flask server and passes model artefacts via en environment variable
	ARTEFACTS_PATH=$(ARTEFACTS_PATH) python predict/predict/app.py

request-test: ## Make a test POST request to flask server (needs to be running, for example having executed flask-server-local)
	curl -v http://0.0.0.0:5000/tag/predict/ -d text="$(TEXT)"

flask-server: ## Run Flask app through its Docker container
	docker run -p 5000:5000 predict

flask-server-debug: ## Run Flask app through its Docker container in DEBUG mode
	docker run -it -p 5000:5000 -v "$PWD":/libraries/app predict

.DEFAULT_GOAL := help
.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'