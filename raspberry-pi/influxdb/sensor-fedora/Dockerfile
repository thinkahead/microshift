FROM docker.io/balenalib/raspberrypi4-64

ENV INITSYSTEM on

RUN apt-get update && apt-get install -yq \
  python3 \
  python3-sense-hat \
  python3-influxdb \
  python3-smbus \
  vim \
  wget && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

COPY sense_hat.py.new /usr/lib/python3/dist-packages/sense_hat/sense_hat.py
COPY . /usr/src/app
WORKDIR /usr/src/app

# Finally, start our app
CMD ["python3", "/usr/src/app/measure.py"]
