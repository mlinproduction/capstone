FROM python:3.7.1

# Add model
COPY ./trained_model /model

# First copy requirements to avoid pip installing libraries each time you change something
COPY ./preprocessing/requirements.txt /libraries/preprocessing/requirements.txt
COPY ./predict/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /libraries/preprocessing/requirements.txt
RUN pip install -r /app/requirements.txt

# Add libraries - things you change more often should go at the end of the Dockerfile 
# in order to make its build more agile
COPY ./preprocessing /libraries/preprocessing
COPY ./predict /app

RUN pip install -e /libraries/preprocessing/
RUN pip install -e /app/

ENV MLINPROD_MODEL_PATH /model
ENV FLASK_APP /app/predict/app.py
ENV FLASK_ENV development
CMD ["flask", "run", "--host=0.0.0.0"]
