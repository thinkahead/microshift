FROM docker.io/dustynv/jetson-inference:r32.6.1
RUN pip install websocket-client
COPY my-detection.py .
CMD python3 my-detection.py
