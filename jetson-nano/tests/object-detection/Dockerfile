FROM docker.io/dustynv/jetson-inference:r32.6.1
RUN apt-get update
RUN apt-get install -y curl
RUN pip install websocket-client
COPY my-detection.py .
COPY my-detection2.py .
COPY runme.sh .
COPY SSD-Mobilenet-v2 data/networks/SSD-Mobilenet-v2
CMD python3 my-detection.py
#CMD ./runme.sh
