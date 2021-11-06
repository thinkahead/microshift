FROM armhf/ubuntu
MAINTAINER karve@us.ibm.com

RUN apt-get update && apt-get install -y curl python-numpy python-pil 
RUN apt-get install -y python-pygame fswebcam
WORKDIR /tmp

RUN curl -LO  https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib-dev_7.2.1-4_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib//librtimulib-utils_7.2.1-4_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib7_7.2.1-4_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/python-rtimulib_7.2.1-4_armhf.deb \
 && curl -LO https://archive.raspberrypi.org/debian/pool/main/p/python-sense-hat/python-sense-hat_2.2.0-1_armhf.deb
 
RUN dpkg -i librtimulib-dev_7.2.1-4_armhf.deb librtimulib-utils_7.2.1-4_armhf.deb librtimulib7_7.2.1-4_armhf.deb python-rtimulib_7.2.1-4_armhf.deb python-sense-hat_2.2.0-1_armhf.deb

RUN rm -f /tmp/*.deb && apt-get clean

ADD test.py /test.py
ADD testcam.py /testcam.py
ADD sparkles.py /sparkles.py
ADD sendimages1.py /sendimages1.py
ADD sendimages2.py /sendimages2.py

WORKDIR /

CMD ["python", "/sendimages1.py"]
