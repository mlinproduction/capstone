# ML In Prod 2020 Capstone

## Requirements


## Setup


## Training a model


## Deploying a trained model



## TODOS

- make predict tests work
- conda env management (global for all modules)
- Separate Dockerfiles for serving and training
- embedding info should be serialized with model to ensure compatibility
- figure out how to include internal dependencies in setup.py
- return proper responses with text/json content-type (https://tedboy.github.io/flask/quickstart/quickstart9.html)
- use proper WSGI instead of Flask's dev server (https://flask.palletsprojects.com/en/1.1.x/deploying/) 
- handle errors gracefully so that a proper response is returned instead of HTML with the stacktrace
- use JSON for POST so that we can pass several text inputs at once
- Write documentation in README's