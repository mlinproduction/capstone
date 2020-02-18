# ML in Production - Capstone 


This repo corresponds to the course of [Machine Learning in Production](https://mlinproduction.github.io/). 
This code is done for educational purposes. As such, it is neither a real production code, nor a toy example easy to 
understand but useless. We tried to make it as similar as possible to real production systems, highlighting some parts and missing
 others to make it more readable. 

## 2020's Edition

In [2020's edition](https://github.com/mlinproduction/capstone/tree/master/2020) we will train a model to tag Stackoverflow's questions. Data is publicly available [here](https://console.cloud.google.com/marketplace/details/stack-exchange/stack-overflow). Basically
- We build a pipeline in [Airflow](https://airflow.apache.org/) to preprocess data in Google's BigQuery.
- We create Python packages, with their corresponding tests, to preprocess text, train a model and predict it.
- We create [Dockerfiles](https://www.docker.com/) that runs a [Flask](https://flask.palletsprojects.com/en/1.1.x/) app that serves the model.
