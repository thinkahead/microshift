FROM balenalib/raspberrypi4-64-debian:latest
RUN apt-get update
#RUN apt-get install -y python3-scipy python3-numpy python3-opencv
RUN apt-get install libblas-dev liblapack-dev gfortran
RUN apt-get install -y python3 python3-pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3
RUN apt-get install -y ffmpeg libsm6 libxext6
COPY requirements_tflite.txt .
COPY requirements_pypi.txt .
RUN pip3 install -r requirements_pypi.txt
RUN pip3 install -r requirements_tflite.txt
RUN apt-get install -y python3-websocket python3-pil python3-rtimulib python3-sense-hat
COPY * .
CMD ./runme.sh
