include predict/predict.conf

TEXT ?= $(TEST_TEXT)

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

.DEFAULT_GOAL := help
.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'