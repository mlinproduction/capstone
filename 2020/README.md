# ML In Prod 2020 Capstone

## Requirements


## Setup


## Training a model


## Deploying a trained model



## TODOS

musts:
-1: revert env variable change:
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