# syntax=docker/dockerfile:1

FROM continuumio/anaconda3

WORKDIR /app

copy . .

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n","3dml", "/bin/bash", "-c"]

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "3dml", "voila", "--enable_nbextensions=True", "index.ipynb"]
