ARG IMAGE_NAME=registry.access.redhat.com/ubi8/ubi-minimal:8.4
# BUILD STAGE
FROM registry.access.redhat.com/ubi8/go-toolset:1.16.7-5 as builder

ARG ARCH=amd64
ARG MAKE_TARGET=cross-build-linux-$ARCH
ARG BIN_TIMESTAMP
ARG SOURCE_GIT_TAG
ARG FROM_SOURCE=false

USER root

LABEL name=microshift-build

ENV GOPATH=/opt/app-root GOCACHE=/mnt/cache GO111MODULE=on

WORKDIR $GOPATH/src/github.com/redhat-et/microshift

COPY . .

# only need these args and the COPY for FROM_SOURCE="true"
ARG MAKE_TARGET
ARG BIN_TIMESTAMP
ARG SOURCE_GIT_TAG

RUN if [ "$FROM_SOURCE" == "true" ]; then \
      make clean $MAKE_TARGET SOURCE_GIT_TAG=$SOURCE_GIT_TAG BIN_TIMESTAMP=$BIN_TIMESTAMP && \
      mv _output/bin/linux_$ARCH/microshift microshift; \
    else \
      export VERSION=$(curl -s https://api.github.com/repos/redhat-et/microshift/releases | grep tag_name | head -n 1 | cut -d '"' -f 4) && \
      curl -LO https://github.com/redhat-et/microshift/releases/download/$VERSION/microshift-linux-$ARCH && \
      mv microshift-linux-$ARCH microshift; \
    fi

#RUN make clean $MAKE_TARGET SOURCE_GIT_TAG=$SOURCE_GIT_TAG BIN_TIMESTAMP=$BIN_TIMESTAMP

# RUN STAGE
FROM ${IMAGE_NAME}
#FROM registry.access.redhat.com/ubi8/ubi-minimal:8.4

ARG ARCH=amd64

RUN microdnf install -y \
    policycoreutils-python-utils \
    iptables \
    && microdnf clean all
#COPY --from=builder /opt/app-root/src/github.com/redhat-et/microshift/_output/bin/linux_$ARCH/microshift /usr/bin/microshift
COPY --from=builder /opt/app-root/src/github.com/redhat-et/microshift/microshift /usr/bin/microshift

ENTRYPOINT ["/usr/bin/microshift"]
CMD ["run"]

# To start:
# podman run --privileged --ipc=host --network=host  \
# -v /var/run:/var/run \
# -v /sys:/sys:ro \
# -v /var/lib:/var/lib:rw,rshared \
# -v /lib/modules:/lib/modules \
# -v /etc:/etc \
# -v /run/containers:/run/containers \
# -v /var/log:/var/log
