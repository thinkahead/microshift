# This Dockerfile should not be run directly. Instead, run ./build-aio-dev.sh
ARG IMAGE_NAME=registry.access.redhat.com/ubi8/ubi-init:8.4

ARG ARCH

FROM ${IMAGE_NAME}

ARG HOST=rhel8

COPY microshift /usr/local/bin/microshift
RUN chmod +x /usr/local/bin/microshift
COPY unit /usr/lib/systemd/system/microshift.service
COPY kubelet-cgroups.conf /etc/systemd/system.conf.d/kubelet-cgroups.conf
COPY crio-bridge.conf /etc/cni/net.d/100-crio-bridge.conf

RUN export VERSION=1.22 && \
    export OS=CentOS_8_Stream && \
    curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/devel:kubic:libcontainers:stable.repo && \
    curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo 

RUN dnf install -y cri-o \
        cri-tools \
        iproute \
        procps-ng && \
    dnf clean all

RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/${ARCH}/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl && \
    sed -i 's|/usr/libexec/crio/conmon|/usr/bin/conmon|' /etc/crio/crio.conf && \
    systemctl enable microshift.service && \
    systemctl enable crio 

RUN curl -s -L https://nvidia.github.io/nvidia-docker/rhel8.3/nvidia-docker.repo | tee /etc/yum.repos.d/nvidia-docker.repo && \
    dnf install nvidia-container-toolkit -y

RUN if [ "$HOST" == "rhel8" ]; then  \
      dnf install -y iptables; \
    else \
      dnf install -y libnetfilter_conntrack libnfnetlink && \
      rpm -v -i --force https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/28/Everything/aarch64/os/Packages/i/iptables-libs-1.6.2-2.fc28.aarch64.rpm \
                   https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/28/Everything/aarch64/os/Packages/i/iptables-1.6.2-2.fc28.aarch64.rpm && \
      sed -e '/mountopt/s/,\?metacopy=on,\?//' -i /etc/containers/storage.conf; \
    fi

COPY nvidia-config.toml /etc/nvidia-container-runtime/config.toml

CMD [ "/sbin/init" ]
