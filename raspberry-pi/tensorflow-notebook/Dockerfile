ARG OWNER=jupyter
ARG BASE_CONTAINER=$OWNER/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Alexei Karve"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
USER root
RUN apt-get update;apt-get upgrade -y;apt-get install -y curl
USER ${NB_USER}
RUN git clone https://github.com/Qengineering/Tensorflow-io.git && cd Tensorflow-io && pip3 install tensorflow_io_gcs_filesystem-0.23.1-cp39-cp39-linux_aarch64.whl && cd .. && rm -rf Tensorflow-io
RUN pip3 install gdown
RUN gdown https://drive.google.com/uc?id=1YpxNubmEL_4EgTrVMu-kYyzAbtyLis29 && pip3 install tensorflow-2.8.0-cp39-cp39-linux_aarch64.whl && rm -rf tensorflow-2.8.0-cp39-cp39-linux_aarch64.whl
RUN pip3 install flask opencv-python-headless==4.5.*
RUN fix-permissions "/home/${NB_USER}"
