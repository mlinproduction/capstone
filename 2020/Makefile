# Good config practices, cf: https://tech.davis-hansson.com/p/make/
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Warning: The following may not work, depending on conda is installed,
# you may need to edit this manually to have the correct CONDA_ROOT
CONDA_ROOT = /$(shell which conda | cut -d "/" -f2)

PIP = $(CONDA_ROOT)/envs/ml_in_prod_capstone/bin/pip
NOSE = $(CONDA_ROOT)/envs/ml_in_prod_capstone/bin/nosetests
PYTHON = $(CONDA_ROOT)/envs/ml_in_prod_capstone/bin/python

ARTEFACTS_PATH ?= train/data/artefacts/final/

# *******************************************************************************************************************
# Setup
# *******************************************************************************************************************

.setup_done: environment.yml
	echo "Using conda at $(CONDA_ROOT)"
	conda env create --force -f environment.yml
	$(PIP) install -e preprocessing/
	$(PIP) install -e train/
	$(PIP) install -e predict/
	$(PIP) install -e custom_airflow/
	$(NOSE) -v preprocessing/tests
	$(NOSE) -v train/tests
	$(NOSE) -v predict/tests
	touch .setup_done

.docker_build: environment.yml $(ARTEFACTS_PATH)
	docker build -t ml_in_prod_capstone:v1.0 . --build-arg artefacts_path=$(ARTEFACTS_PATH)

.PHONY: setup
setup: .setup_done .docker_build ## Creates project environment, installs packages, runs tests and builds the docker image

.PHONY: test
test: ## Runs package tests
	$(NOSE) -v preprocessing/tests
	$(NOSE) -v train/tests
	$(NOSE) -v predict/tests

# *******************************************************************************************************************
# Training
# *******************************************************************************************************************

DATASET_DEFAULT = train/data/stackoverflow_posts.csv
DATASET ?= $(DATASET_DEFAULT)

$(DATASET_DEFAULT):
	curl -L -o $(DATASET_DEFAULT) "https://docs.google.com/uc?export=download&id=1ud6JR2JjkRi-iRrsx8kWj4rPL5BVt5Pd"

.PHONY: download ## Downloads the stackoverflow (post, tag) data to train the model
download: $(DATASET_DEFAULT)

$(ARTEFACTS_PATH): $(DATASET) .setup_done train/train/run.py
	echo "Training model and saving into `$(ARTEFACTS_PATH)`"
	$(PYTHON) train/train/run.py $(ARTEFACTS_PATH) $(DATASET) train/conf/train-conf.yml

.PHONY: train
train: $(ARTEFACTS_PATH) ## Trains a model to predict tags for stack overflow posts

# *******************************************************************************************************************
# Prediction / deployment targets
# *******************************************************************************************************************

# Text you want to use for testing, provide via `make CMD TEXT="abcd"`
TEXT ?= ruby on rails: how to change BG color of options in select list, ruby-on-rails

.PHONY: predict-test
predict-test: .setup_done $(ARTEFACTS_PATH) ## Calling predict from terminal
	$(PYTHON) predict/predict/run.py $(ARTEFACTS_PATH) --text="$(TEXT)"

.PHONY: flask-server-local
flask-server-local: .setup_done $(ARTEFACTS_PATH) ## Starts flask server and passes model artefacts through an environment variable
	ARTEFACTS_PATH=$(ARTEFACTS_PATH) python predict/predict/app.py

.PHONY: request-test
request-test: ## Make a test POST request to flask server (needs to be running, for example having executed flask-server-local)
	curl -v http://0.0.0.0:5000/tag/predict/ -d text="$(TEXT)"

.PHONY: flask-server-docker
flask-server-docker: .docker_build ## Run Flask app through its Docker container
	docker run -p 5000:5000  ml_in_prod_capstone:v1.0

.PHONY: flask-server-docker-debug
flask-server-docker-debug: .docker_build ## Run Flask app through its Docker container in DEBUG mode
	docker run -it -p 5000:5000 -v ml_in_prod_capstone:v1.0

.DEFAULT_GOAL := help
.PHONY: help
help: ## Displays makefile commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

_all: flask-server-local flask-server-docker

.PHONY: graph
graph:  ## plots makefile dependency graph into `makefile_graph.png`
	$(MAKE) _all --dry-run -Bnd | make2graph | dot -Tpng -o makefile_graph.png
