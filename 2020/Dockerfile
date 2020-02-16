FROM continuumio/miniconda:latest

COPY environment.yml /lib/environment.yml
COPY ./preprocessing /lib/preprocessing
COPY ./train /lib/train
COPY ./predict /lib/predict

RUN /opt/conda/bin/conda env create -f /lib/environment.yml

RUN echo "source activate ml_in_prod_capstone" > ~/.bashrc
ENV PATH /opt/conda/envs/ml_in_prod_capstone/bin:$PATH

RUN /opt/conda/envs/ml_in_prod_capstone/bin/pip install -e /lib/preprocessing/
RUN /opt/conda/envs/ml_in_prod_capstone/bin/pip install -e /lib/train/
RUN /opt/conda/envs/ml_in_prod_capstone/bin/pip install -e /lib/predict/

# clean up unused stuff
RUN /opt/conda/bin/conda clean -afy

# Copy the model into the /model folder
ARG artefacts_path
COPY $artefacts_path /model


ENV MLINPROD_MODEL_PATH /model
ENV FLASK_APP /app/predict/app.py
ENV FLASK_ENV development

CMD ["python", "/lib/predict/predict/app.py", "--artefacts_path=/model"]
