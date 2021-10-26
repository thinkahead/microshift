FROM nvcr.io/nvidia/l4t-base:r32.6.1

RUN apt-get update && apt-get install -y --no-install-recommends make g++
COPY ./samples /tmp/samples

WORKDIR /tmp/samples/0_Simple/vectorAdd/
RUN make clean && make

CMD ["./vectorAdd"]

