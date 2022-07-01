FROM docker.io/balenalib/raspberrypi4-64

ENV INITSYSTEM on

RUN apt-get update && apt-get install -yq \
  python3 \
  python3-sense-hat \
  libicu-dev \
  vim git wget && \
  apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
COPY sensehat-quickstart-1.sh /usr/src/app
RUN bash -c /usr/src/app/sensehat-quickstart-1.sh

COPY sensehat-quickstart-2.sh /usr/src/app

# Finally, start our app
CMD ["bash", "-c", ". ~/.bashrc;/usr/src/app/sensehat-quickstart-2.sh"]
