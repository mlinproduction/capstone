include predict/predict.conf

DATASET_DEFAULT=train/data/bq-results-20200205-092131-ioej0ewh4vcc_large.csv

TEXT ?= $(TEST_TEXT)
DATASET ?= $(DATASET_DEFAULT)

predict-test: ## Calling predict from terminal
	python predict/predict/run.py $(ARTEFACTS_PATH) --text="$(TEXT)"

flask-server-local: ## Starts flask server and passes model artefacts via en environment variable
	ARTEFACTS_PATH=$(ARTEFACTS_PATH) python predict/predict/app.py

request-test: ## Make a test POST request to flask server (needs to be running, for example having executed flask-server-local)
	curl -v http://0.0.0.0:5000/tag/predict/ -d text="$(TEXT)"

flask-server: ## Run Flask app through its Docker container
	docker run -p 5000:5000 predict

flask-server-debug: ## Run Flask app through its Docker container in DEBUG mode
	docker run -it -p 5000:5000 -v "$PWD":/libraries/app predict

$(DATASET_DEFAULT):
	curl -L -o $(DATASET_DEFAULT) 'https://docs.google.com/uc?export=download&id=1ud6JR2JjkRi-iRrsx8kWj4rPL5BVt5Pd'

.PHONY: download
download: $(DATASET_DEFAULT)

train: $(DATASET)
	python train/train/run.py train/data/artefacts $(DATASET) train/conf/train-conf.yml

.DEFAULT_GOAL := help
.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'