#FROM armhf/ubuntu
FROM docker.io/arm32v7/ubuntu
MAINTAINER karve@us.ibm.com

RUN apt-get update && apt-get install -y curl python-numpy python-pil 
RUN apt-get install -y python-pygame fswebcam
RUN apt-get install -y python-websocket
RUN apt-get install -y python
WORKDIR /tmp

RUN curl -LO  https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib-dev_7.2.1-5_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib//librtimulib-utils_7.2.1-5_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib7_7.2.1-5_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/python-rtimulib_7.2.1-5_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/p/python-sense-hat/python-sense-hat_2.2.0-1_armhf.deb
RUN python --version 
RUN dpkg -i librtimulib-dev_7.2.1-5_armhf.deb librtimulib-utils_7.2.1-5_armhf.deb librtimulib7_7.2.1-5_armhf.deb python-rtimulib_7.2.1-5_armhf.deb python-sense-hat_2.2.0-1_armhf.deb

RUN rm -f /tmp/*.deb && apt-get clean

ADD temperature.py /temperature.py
ADD testcam.py /testcam.py
ADD sparkles.py /sparkles.py
ADD sendimages1.py /sendimages1.py
ADD sendimages2.py /sendimages2.py
ADD sendtonodered.py /sendtonodered.py
#RUN pip install websocket-client

WORKDIR /

CMD ["python", "/sendtonodered.py"]
