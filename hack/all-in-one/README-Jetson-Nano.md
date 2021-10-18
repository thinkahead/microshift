# Microshift on Jetson Nano
We can run Microshift directly on Ubuntu 18.04 Jetson Nano or within a Docker RHEL8 container on Jetson Nano, the latter is easier. Both options are described. I suggest using the 128GB microSDXC card so that you have sufficient space for experimentation, but Microshift works with the 32GB card.

## Update and Test the Jetson Nano
### Updating your Jetson nano to new Minor Release
Jetson Nano downloads are at https://developer.nvidia.com/embedded/downloads and OS information at https://developer.nvidia.com/embedded/jetpack

If your SD card has older Jetpak, you can update the L4T as follows. The latest is JetPack 4.6 that includes L4T 32.6.1. The platform is t210 for NVIDIA® Jetson Nano™ devices. The version is set to r32.6 (Do not set to r32.6.1)
```
sudo su -
vi /etc/apt/sources.list.d/nvidia-l4t-apt-source.list

deb https://repo.download.nvidia.com/jetson/common r32.6 main
deb https://repo.download.nvidia.com/jetson/t210 r32.6 main

apt update
apt dist-upgrade

pip install -U jetson-stats
jetson_release -v
jtop
cat /etc/nv_tegra_release

# If your hostname is without a domain, you may want to add the ".example.com"
# There was an issue on microshift saying that this is required
# I don't think adding the domain is necessary anymore, but might as well do it
hostnamectl set-hostname jetson-nano.example.com # replace jetson-nano with your short hostname
dpkg-reconfigure tzdata # Select your timezone

# If you have the default Jupyter Lab running on your Jetson nano, you may stop it
systemctl stop jetcard_jupyter.service
# systemctl restart nvargus-daemon # If camera is not working
```

### Testing the Jupyter Lab container in docker
DLI "Getting Started with AI on Jetson Nano" Course Environment Container https://ngc.nvidia.com/catalog/containers/nvidia:dli:dli-nano-ai
```
docker run --runtime nvidia -it --rm --network host --volume ~/nvdli-data:/nvdli-nano/data --device /dev/video0 nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.6.1
```
Connect to your Jetson nano ip address and login with password dlinano [http://192.168.1.205:8888/lab?](http://192.168.1.205:8888/lab?)

You can run the notebook /hello_camera/usb_camera.ipynb and test the camera. After testing, release the camera resource and shutdown the kernel.

### Testing the USB camera attached to Jetson Nano with gstreamer on Mac
On Mac
- Install gstreamer pkg from https://gstreamer.freedesktop.org/data/pkg/osx/1.19.2/
- Install gst-libav
```
brew install gst-libav
```

On Jetson Nano
```
video-viewer --bitrate=1000000 /dev/video0 rtp://192.168.1.185:1234  # 192.168.1.185 is the IP address of Mac
```

On Mac
```
gst-launch-1.0 -v udpsrc port=1234 \
 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! \
 rtph264depay ! decodebin ! videoconvert ! autovideosink
```

## Install dependencies and build Microshift binary for arm64 on Ubuntu 18.04 - Jetson Nano
You may either copy the microshift binary from the docker image docker.io/karve/microshift:arm64-jetsonnano for the jetson nano or build it.

### Copy the Microshift binary from docker image
If you want to build your own microshift binary for arm64 Jetson Nano, you may skip this step.
```
dlinano@jetson-nano:~$ id=$(docker create docker.io/karve/microshift:arm64-jetsonnano)
dlinano@jetson-nano:~$ docker cp $id:/usr/local/bin/microshift /usr/local/bin/microshift
dlinano@jetson-nano:~$ microshift version
Microshift Version: 4.7.0-0.microshift-2021-08-31-224727-52-g87d6da6
Base OKD Version: 4.7.0-0.okd-2021-06-13-090745
dlinano@jetson-nano:~$ docker rm -v $id
```

### Install the dependencies
Run as root
```
# We will not use docker to build any binaries, stop it to reduce memory consumption
# Delete any docker container and images if you are using a 32GB microSDXC to save space
docker rmi nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.6.1
systemctl stop docker;systemctl stop docker.socket

apt -y install build-essential curl libgpgme-dev pkg-config libseccomp-dev

# Install golang
wget https://golang.org/dl/go1.17.2.linux-arm64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.2.linux-arm64.tar.gz
rm -f go1.17.2.linux-arm64.tar.gz
export PATH=$PATH:/usr/local/go/bin
export GOPATH=/root/go
# Add above 2 lines to /root/.bashrc
mkdir $GOPATH
```

### Build the Microshift binary
Build the binary on your Jetson Nano. You may skip this if you copied the binary from the docker image earlier.
```
git clone https://github.com/redhat-et/microshift.git
cd microshift
make
ls -las microshift # binary in current directory /root/microshift
cp microshift /usr/local/bin/.
rm -rf /root/.cache/go-build # Optional Cleanup
cd ..
#rm -rf microshift # You can delete this folder, we have copied the microshift arm64 binary to /usr/local/bin
```

## Running Microshift directly on the Jetson Nano
Build the Microshift binary as above. The following instructions follow the steps in the install.sh in the microshift directory (you can use that as reference if required).

### Install the dependencies
```
OS_VERSION=18.04
CRIOVERSION=1.22
OS=xUbuntu_$OS_VERSION
KEYRINGS_DIR=/usr/share/keyrings
echo "deb [signed-by=$KEYRINGS_DIR/libcontainers-archive-keyring.gpg] https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list > /dev/null
echo "deb [signed-by=$KEYRINGS_DIR/libcontainers-crio-archive-keyring.gpg] http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$CRIOVERSION/$OS/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$CRIOVERSION.list > /dev/null
mkdir -p $KEYRINGS_DIR
rm -f /usr/share/keyrings/libcontainers-archive-keyring.gpg
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo gpg --dearmor -o $KEYRINGS_DIR/libcontainers-archive-keyring.gpg
rm -f /usr/share/keyrings/libcontainers-crio-archive-keyring.gpg
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$CRIOVERSION/$OS/Release.key | sudo gpg --dearmor -o $KEYRINGS_DIR/libcontainers-crio-archive-keyring.gpg

apt install -y btrfs-tools containers-common libassuan-dev libdevmapper-dev libglib2.0-dev libc6-dev libgpgme-dev libgpg-error-dev libseccomp-dev libsystemd-dev libselinux1-dev pkg-config go-md2man libudev-dev software-properties-common gcc make curl
ls /usr/include/gpgme.h
apt-get install -y policycoreutils-python-utils conntrack firewalld
```
You canot install cri-o from the kubic above, it needs to be built for Ubuntu 18.04 for arm64.

### Build conmon, cri-o, crictl and containernetworking plugins. Get the kubeconfig for arm64

Need to test again if this single line script works for installing cri-o, crictl and plugins, if not, then the rest of the instructions are below. If it works, jump to "Setup firewalld" section.
```
curl https://raw.githubusercontent.com/cri-o/cri-o/main/scripts/get | bash -s -- -a arm64
```

Reference https://github.com/cri-o/cri-o/blob/main/install.md#installing-crio
```
git clone https://github.com/containers/conmon
cd conmon
make
make install
cd ..
rm -rf conmon

git clone https://github.com/cri-o/cri-o.git
cd cri-o/
make
make install
crio version
make install.config
make install.systemd
cd ..
rm -rf cri-o

systemctl daemon-reload
systemctl enable crio
cat /etc/crio/crio.conf
rm -f /etc/crio/crio.conf # I think you must delete this, the file is empty anyway

# Create the /etc/crio/crio.conf.d/01-crio-runc.conf - Is this required?
mkdir /etc/crio/crio.conf.d
cat << EOF > /etc/crio/crio.conf.d/01-crio-runc.conf
[crio.runtime.runtimes.runc]
runtime_path = "/usr/sbin/runc"
runtime_type = "oci"
runtime_root = "/run/runc"
EOF

git clone https://github.com/kubernetes-sigs/cri-tools.git
cd cri-tools
make
make install
cd ..
rm -rf cri-tools

# When does /etc/containers/storage.conf get created? If it is not created here, this step may come later
# We need to remove the options for mountopt from /etc/containers/storage.conf to the invalid argument error
# "creating overlay mount to /var/lib/containers/storage/overlay/.../merged, mount_data="nodev,metacopy=on,lowerdir=/var/lib/containers/storage/overlay...": invalid argument
sed -i "s/^\(mountopt.*\)/#\\1/" /etc/containers/storage.conf

# Get kubectl
ARCH=arm64
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/$ARCH/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin
```

### Install CNI plugins
Reference https://github.com/cri-o/cri-o/blob/main/contrib/cni/README.md
```
# We use the type bridge
git clone https://github.com/containernetworking/plugins.git
cd plugins/
./build_linux.sh
mkdir -p /opt/cni/bin
cp bin/* /opt/cni/bin
cd ..
```

### Create the policy.json and registries.conf
/etc/containers/policy.json
```
{ "default": [{ "type": "insecureAcceptAnything" }] }
```

/etc/containers/registries.conf
```
[registries.search]
registries = ['registry.access.redhat.com', 'registry.fedoraproject.org', 'quay.io', 'docker.io']

[registries.insecure]
registries = []

[registries.block]
registries = []
```

### Setup firewalld
```
systemctl enable firewalld --now
firewall-cmd --zone=public --permanent --add-port=6443/tcp
firewall-cmd --zone=public --permanent --add-port=30000-32767/tcp
firewall-cmd --zone=public --permanent --add-port=2379-2380/tcp
firewall-cmd --zone=public --add-masquerade --permanent
firewall-cmd --zone=public --add-port=10250/tcp --permanent
firewall-cmd --zone=public --add-port=10251/tcp --permanent
firewall-cmd --zone=public --add-port=8888/tcp --permanent $ For Jupyterlab Course
firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16
firewall-cmd --reload
```

### CRI-O config to match Microshift networking values
```
sh -c 'cat << EOF > /etc/cni/net.d/100-crio-bridge.conf
{
    "cniVersion": "0.4.0",
    "name": "crio",
    "type": "bridge",
    "bridge": "cni0",
    "isGateway": true,
    "ipMasq": true,
    "hairpinMode": true,
    "ipam": {
        "type": "host-local",
        "routes": [
            { "dst": "0.0.0.0/0" }
        ],
        "ranges": [
            [{ "subnet": "10.42.0.0/24" }]
        ]
    }
}
EOF'

systemctl restart crio
systemctl status crio
journalctl -u crio -f # Ctrl-C to stop the logs
```

### Add the nvidia-container-runtime-hook to cri-o
Create the /usr/share/containers/oci/hooks.d/nvidia.json
```
  {
      "version": "1.0.0",
      "hook": {
          "path": "/usr/bin/nvidia-container-runtime-hook",
          "args": ["nvidia-container-runtime-hook", "prestart"],
          "env": [
              "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin              "
          ]
      },
      "when": {
          "always": true,
          "commands": [".*"]
      },
      "stages": ["prestart"]
  }
```

Restart cri-o
```
systemctl restart crio
```

### CRI-O samples

#### 1. cri-o with nginx sample
Use this section to learn how to create/delete a pod with container using cri-o
```
cat >nginx.json<<EOF
{
  "metadata": {
    "name": "nginx-container",
    "attempt": 1
  },
  "image": {
    "image": "nginx"
  },
  "log_path": "nginx.log",
  "linux": {
    "security_context": {
      "namespace_options": {}
    }
  }
}
EOF

cat >net-pod.json<<EOF
{
  "metadata": {
    "name": "networking",
    "uid": "networking-pod-uid",
    "namespace": "default",
    "attempt": 1
  },
  "hostname": "networking",
  "port_mappings": [
    {
      "container_port": 80
    }
  ],
  "log_directory": "/tmp/net-pod",
  "linux": {}
}
EOF

crictl runp net-pod.json
crictl pods # Get the podid
crictl pull nginx # Pull the image
crictl images # This will show the nginx image
crictl create $podid nginx.json net-pod.json # The container for nginx will go into Created state
crictl ps -a # List containers, get the containerid
crictl start $containerid # Go to Running state
crictl logs $containerid

crictl inspectp $podid | grep io.kubernetes.cri-o.IP.0 # Get the ipaddr of pod
curl $ipaddr # Will return the "Welcome to nginx!" html

crictl stop $containerid # Go to Exited state
crictl ps -a
crictl rm $containerid
crictl stopp $podid # Stop the pod
crictl rmp $podid # Remove the pod
```

#### 2. cri-o with vector-add cuda sample
Copy the samples (we use the vectorAdd)
```
mkdir vectoradd
cd vectoradd
cp -r /usr/local/cuda/samples .
```

Create the following Dockerfile
```
FROM nvcr.io/nvidia/l4t-base:r32.6.1

RUN apt-get update && apt-get install -y --no-install-recommends make g++
COPY ./samples /tmp/samples

WORKDIR /tmp/samples/0_Simple/vectorAdd/
RUN make clean && make

CMD ["./vectorAdd"]
```

Create the vectoradd.json
```
{
  "metadata": {
    "name": "vectoradd-container",
    "attempt": 1
  },
  "image": {
    "image": "docker.io/karve/vector-add-sample:arm64-jetsonnano"
  },
  "log_path": "vectoradd.log",
  "linux": {
    "security_context": {
      "namespace_options": {}
    }
  }
}
```

Create the net-pod.json
```
{
  "metadata": {
    "name": "networking",
    "uid": "networking-pod-uid",
    "namespace": "default",
    "attempt": 1
  },
  "hostname": "networking",
  "port_mappings": [
    {
      "container_port": 80
    }
  ],
  "log_directory": "/tmp/net-pod",
  "linux": {}
}
```

Build and push the vector-add-sample image
```
docker build -t karve/vector-add-sample:arm64-jetsonnano .
docker push karve/vector-add-sample:arm64-jetsonnano
```

Run the vector-add-sample in crio
```
crictl runp net-pod.json
crictl pods # Get the podid
crictl pull docker.io/karve/vector-add-sample:arm64-jetsonnano
crictl images # This will show the vector-add-sample image
crictl create $podid vectoradd.json net-pod.json # The container for nginx will go into Created state
crictl ps -a # List containers, get the containerid
crictl start $containerid # Go to Running and Exited state
crictl logs $containerid
```
The output shows: Test PASSED
```
root@jetson-nano:~/tests/matmul# crictl logs 681ed5500e2bc
[Vector addition of 50000 elements]
Copy input data from the host memory to the CUDA device
CUDA kernel launch with 196 blocks of 256 threads
Copy output data from the CUDA device to the host memory
Test PASSED
Done
```

If it fails because of missing hook /usr/share/containers/oci/hooks.d/nvidia.json, you will see the output
```
Failed to allocate device vector A (error code CUDA driver version is insufficient for CUDA runtime version)!
[Vector addition of 50000 elements]
```

Delete the container and pod
```
crictl ps -a
crictl rm $containerid
crictl stopp $podid # Stop the pod
crictl rmp $podid # Remove the pod
```

#### 3. cri-o with device-query sample
Create the following Dockerfile in new folder devicequery and follow the same instructions as vector-add
```
FROM nvcr.io/nvidia/l4t-base:r32.6.1

RUN apt-get update && apt-get install -y --no-install-recommends make g++
COPY ./samples /tmp/samples

WORKDIR /tmp/samples/1_Utilities/deviceQuery
RUN make clean && make

CMD ["./deviceQuery"]
```

Output
```
./deviceQuery Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

Detected 1 CUDA Capable device(s)

Device 0: "NVIDIA Tegra X1"
  CUDA Driver Version / Runtime Version          10.2 / 10.2
  CUDA Capability Major/Minor version number:    5.3
  Total amount of global memory:                 3956 MBytes (4148273152 bytes)
  ( 1) Multiprocessors, (128) CUDA Cores/MP:     128 CUDA Cores
  GPU Max Clock rate:                            922 MHz (0.92 GHz)
  Memory Clock rate:                             13 Mhz
  Memory Bus Width:                              64-bit
  L2 Cache Size:                                 262144 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(65536), 2D=(65536, 65536), 3D=(4096, 4096, 4096)
  Maximum Layered 1D Texture Size, (num) layers  1D=(16384), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(16384, 16384), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 32768
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 1 copy engine(s)
  Run time limit on kernels:                     Yes
  Integrated GPU sharing Host Memory:            Yes
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Disabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Compute Preemption:            No
  Supports Cooperative Kernel Launch:            No
  Supports MultiDevice Co-op Kernel Launch:      No
  Device PCI Domain ID / Bus ID / location ID:   0 / 0 / 0
  Compute Mode:
     < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >

deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 10.2, CUDA Runtime Version = 10.2, NumDevs = 1
Result = PASS
```

#### 4. Testing cri-o with pytorch sample
**This will stress test the GPU - Warning: attach the FAN**

Create the pytorchsample.json
```
{
  "metadata": {
    "name": "pytorchsample-container",
    "attempt": 1
  },
  "image": {
    "image": "nvcr.io/nvidia/l4t-pytorch:r32.6.1-pth1.9-py3"
  },
  "log_path": "pytorchsample.log",
  "linux": {
    "security_context": {
      "namespace_options": {}
    }
  }
}
```

Run the pytorch sample
```
crictl runp net-pod.json
crictl pods # Get the podid
crictl pull nvcr.io/nvidia/l4t-pytorch:r32.6.1-pth1.9-py3
crictl images # This will show the l4t-pytorch image
crictl create $podid pytorchsample.json net-pod.json # The container for nginx will go into Created state
crictl exec -it $podid bash

echo "nameserver 8.8.8.8" > /etc/resolv.conf
TA_URL="https://nvidia.box.com/shared/static/y1ygiahv8h75yiyh0pt50jqdqt7pohgx.gz"
DATA_NAME="ILSVRC2012_img_val_subset_5k"
DATA_PATH="test/data/$DATA_NAME"
if [ ! -d "$DATA_PATH" ]; then
 echo 'downloading data for testing torchvision...'
 if [ ! -d "test/data" ]; then
  mkdir -p test/data
 fi
 wget --quiet --show-progress --progress=bar:force:noscroll --no-check-certificate $DATA_URL -O test/data/$DATA_NAME.tar.gz
 tar -xzf test/data/$DATA_NAME.tar.gz -C test/data/
fi
wget https://raw.githubusercontent.com/dusty-nv/jetson-containers/master/test/test_pytorch.py -O test/test_pytorch.py
python3 test/test_pytorch.py
python3 test/test_torchvision.py --data=$DATA_PATH --use-cuda
wget https://raw.githubusercontent.com/dusty-nv/jetson-containers/master/test/test_torchaudio.py -O test/test_torchaudio.py
python3 test/test_torchaudio.py
exit
```

Delete the container and pod for pytorch
```
crictl ps -a
crictl rm $containerid
crictl stopp $podid # Stop the pod
crictl rmp $podid # Remove the pod
```

### Run Microshift
```
mkdir /var/hpvolumes # used by hostpath-provisioner
cp /root/microshift /usr/local/bin/. # If not already done

mkdir /usr/lib/systemd/system
cat << EOF | sudo tee /usr/lib/systemd/system/microshift.service
[Unit]
Description=Microshift
After=crio.service

[Service]
WorkingDirectory=/usr/local/bin/
ExecStart=/usr/local/bin/microshift run
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

#sed -i 's|^ExecStart=microshift|ExecStart=/usr/local/bin/microshift|' /usr/lib/systemd/system/microshift.service
systemctl daemon-reload
systemctl start microshift
systemctl status microshift
journalctl -u microshift -f # Ctrl-C to break

mkdir -p $HOME/.kube
if [ -f $HOME/.kube/config ]; then
    mv $HOME/.kube/config $HOME/.kube/config.orig
fi
KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig:$HOME/.kube/config.orig /usr/local/bin/kubectl config view --flatten > $HOME/.kube/config
watch "kubectl get nodes;kubectl get pods -A;crictl pods;crictl images"
```

### Output when microshift is started properly
```
Every 2.0s: kubectl get nodes;kubectl get pods -A;crictl images;crictl pods                                           jetson-nano.example.com: Mon Oct 11 11:59:46 2021

NAME                      STATUS   ROLES    AGE    VERSION
jetson-nano.example.com   Ready    <none>   6m3s   v1.20.1
NAMESPACE                       NAME                                  READY   STATUS    RESTARTS   AGE
kube-system                     kube-flannel-ds-fzfn6                 1/1     Running   0          5m24s
kubevirt-hostpath-provisioner   kubevirt-hostpath-provisioner-98frt   1/1     Running   0          5m26s
openshift-dns                   dns-default-bd92w                     3/3     Running   0          5m25s
openshift-ingress               router-default-79f7dc4c6b-2p4nb       1/1     Running   0          5m25s
openshift-service-ca            service-ca-58798776fb-b7dkb           1/1     Running   0          5m26s
IMAGE                                     TAG                 IMAGE ID            SIZE
k8s.gcr.io/pause                          3.6                 7d46a07936af9       492kB
quay.io/microshift/coredns                1.6.9               2e234fad5a864       264MB
quay.io/microshift/flannel                v0.14.0             996759f548df5       149MB
quay.io/microshift/hostpath-provisioner   v0.9.0              e96859fbded4f       39.2MB
quay.io/microshift/kube-rbac-proxy        v0.11.0             03509ac20d4d7       41.5MB
quay.io/microshift/openshift-router       4.5                 2ade343656684       123MB
quay.io/microshift/service-ca-operator    latest              0fedc7575c705       152MB
POD ID              CREATED             STATE               NAME                                  NAMESPACE                       ATTEMPT             RUNTIME
d1dcfec0e2bc2       4 minutes ago       Ready               dns-default-bd92w                     openshift-dns                   0                   (default)
e02d8d7847572       4 minutes ago       Ready               router-default-79f7dc4c6b-2p4nb       openshift-ingress               0                   (default)
a9ae0fe8b5a14       5 minutes ago       Ready               kube-flannel-ds-fzfn6                 kube-system                     0                   (default)
bd375903e4d38       5 minutes ago       Ready               kubevirt-hostpath-provisioner-98frt   kubevirt-hostpath-provisioner   0                   (default)
b1331d994b844       5 minutes ago       Ready               service-ca-58798776fb-b7dkb           openshift-service-ca            0                   (default)
```

### Use the oc client
```
wget https://mirror.openshift.com/pub/openshift-v4/arm64/clients/ocp/candidate/openshift-client-linux.tar.gz
tar -zxvf ../openshift-client-linux.tar.gz
cp oc /usr/local/bin
# export the correct KUBECONFIG
oc get pods -A
```

### Errors
#### 1. The node was low on resource: [DiskPressure]
If you have less than 10% free disk space on the microSDXC card, the kubevirt-hostpath-provisioner pod may get evicted. This will happen on the 32GB microSDXC card if the disk space cannot be reclaimed after deleting usused images. You will need to create space by deleting some github sources we had downloaded for installation.
```
rm -rf /root/.cache/go-build # Cleanup to get space on microSDXC card
# You can check the eviction events as follows
kubectl describe nodes
kubectl get events --field-selector involvedObject.kind=Node
kubectl delete events --field-selector involvedObject.kind=Node
```

#### 2. ImageInspectError
If the pod shows this ImageInspectError state, you may be missing the /etc/containers/registries.conf. You can add that or qualify the image with "docker.io/"  or the correct registry.

#### 3. oc new-project image-stream command don't work
See https://github.com/redhat-et/microshift/issues/240
```
root@jetson-nano:~# oc new-project alexei
error: unable to default to a user name: the server could not find the requested resource (get users.user.openshift.io ~)
```

#### 4. Error: failed to initialize NVML: could not load NVML library
https://github.com/NVIDIA/k8s-device-plugin/issues/19
The nvidia-device-plugin does not work on Jetson Nano. So, directly add the nvidia-container-runtime-hook to cri-o as specified at https://github.com/thinkahead/microshift/blob/main/hack/all-in-one/README-Jetson-Nano.md#add-the-nvidia-container-runtime-hook-to-cri-o
```
root@jetson-nano:~/k8s-device-plugin# docker run -it --privileged --network=none -v /var/lib/kubelet/device-plugins:/var/lib/kubelet/device-plugins docker.io/karve/k8s-device-plugin:arm64-jetsonnano --pass-device-specs
2021/10/13 16:34:03 Loading NVML
2021/10/13 16:34:03 Failed to initialize NVML: could not load NVML library.
2021/10/13 16:34:03 If this is a GPU node, did you set the docker default runtime to `nvidia`?
2021/10/13 16:34:03 You can check the prerequisites at: https://github.com/NVIDIA/k8s-device-plugin#prerequisites
2021/10/13 16:34:03 You can learn how to set the runtime at: https://github.com/NVIDIA/k8s-device-plugin#quick-start
2021/10/13 16:34:03 If this is not a GPU node, you should set up a toleration or nodeSelector to only deploy this plugin on GPU nodes
2021/10/13 16:34:03 Error: failed to initialize NVML: could not load NVML library
```

### Cleanup microshift/cri-o images and pods
```
systemctl stop microshift
crictl rm --all --force
crictl rmp --all --force
crictl rmi --all
pkill -9 conmon
pkill -9 pause
rm -rf /var/lib/microshift
systemctl stop crio
rm -rf /var/lib/containers/*
systemctl start crio
```

## Running Microshift in docker container on Ubuntu 18.04 - Jetson Nano
Build microshift binary as mentioned in previous section. You will copy the microshift binary for creating the image.

### Build the Microshift docker image on Jetson Nano
Build the microshift image on your Jetson Nano. You may skip this if you pulled the docker image earlier. The Dockerfile uses the registry.access.redhat.com/ubi8/ubi-init:8.4 as the default base image. One fix is required to the Dockerfile to replace the hardcoded x86_64 with aarch64. I have created an image at docker.io/karve/microshift:arm64-jetsonnano
```
systemctl start docker
git clone https://github.com/thinkahead/microshift.git
cd microshift/hack/all-in-one
cp /root/microshift/microshift . # copy the microshift binary built earlier to this folder
# Replace the two lines containing x86_64 with aarch64 in Dockerfile
      rpm -v -i --force https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/28/Everything/aarch64/os/Packages/i/iptables-libs-1.6.2-2.fc28.aarch64.rpm \
                   https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/28/Everything/aarch64/os/Packages/i/iptables-1.6.2-2.fc28.aarch64.rpm && \

# HOST=xxx below should not be rhel8, so I just set it to ubuntu18
docker build --build-arg HOST=ubuntu18 -t microshift .
```

### Start the microshift container and exec into it, check the node and pods from within the container
```
docker volume rm microshift-data;docker volume create microshift-data
docker run -d --rm --name microshift -h microshift.example.com --privileged -v /lib/modules:/lib/modules -v microshift-data:/var/lib -p 6443:6443 microshift # or use the docker.io/karve/microshift:arm64-jetsonnano
# If 6443 port is in use on the Jetson Nano, you may use -p 9443:6443
docker exec -it microshift bash
# Within the container
export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig 
watch "kubectl get nodes;kubectl get pods -A;crictl images;crictl pods" # wait for 2 minutes

# If the openshift-ingress and openshift-dns keep restarting, lets fix it. If not, exit the container - All good.
systemctl stop microshift
crictl rm --all --force
crictl rmp --all --force
crictl rmi --all
pkill -9 conmon
pkill -9 pause
rm -rf /var/lib/microshift
systemctl start microshift

exit
```

Outside the container back on the Jetson Nano    

On jetson-nano (if you installed firewalld previously, ignore otherwise). Use the appropriate port 9443 or 6443.
```
firewall-cmd --zone=public --list-ports # Check if require port 9443 or 6443 is present
firewall-cmd --zone=public --permanent --add-port=9443/tcp
firewall-cmd --reload
```

Access the nodes and pods in the container from outside the container. Note that the microshift container must be started and microshift should be running within the container.
```
export KUBECONFIG=$(docker volume inspect microshift-data --format "{{.Mountpoint}}")/microshift/resources/kubeadmin/kubeconfig
#export KUBECONFIG=/var/lib/docker/volumes/microshift-data/_data/microshift/resources/kubeadmin/kubeconfig
# if you changed the port on the host side to 9443, you will need to replace the port in the kubeconfig. The default is 6443
kubectl get pods -A
```

### Use the prebuilt Microshift arm64 image from quay.io
Specifically, we use the quay.io/microshift/microshift:4.7.0-0.microshift-2021-08-31-224727-aio-linux-arm64 image.
The arm64 image from https://quay.io/repository/microshift/microshift?tab=tags did not work in Docker on Jetson Nano. I got the error with iptables with the quay.io/microshift/microshift:4.7.0-0.microshift-2021-08-31-224727-aio-linux-arm64 when the container was started and the pods within the microshift container stayed in ContainerCreating state.
```
Oct 07 14:38:21 microshift.example.com microshift[78]: E1007 14:38:21.128486      78 proxier.go:874] Failed to ensure that filter chain KUBE-EXTERNAL-SERVICES exists: error creating chain "KUBE-EXTERNAL-SERVICES": exit status 4: iptables v1.8.4 (nf_tables): Could not fetch rule set generation id: Invalid argument

Oct 07 14:38:22 microshift.example.com microshift[78]: W1007 14:38:22.321539      78 iptables.go:564] Could not set up iptables canary mangle/KUBE-PROXY-CANARY: error creating chain "KUBE-PROXY-CANARY": exit status 4: iptables v1.8.4 (nf_tables): Could not fetch rule set generation id: Invalid argument
```

Also I got golang errors with the microshift binary from this container when I tried to use it directly on Jetson Nano (haven't tried to use the microsoft binary directly again).

I don't see the above iptables problems now on Oct 11, 2021. The iptables rpms in the image look correct now (1.8.7-3). Previously there was a mismatch between rhel8 and fedora iptables on my setup. Maybe I forgot to delete the docker volume as I was switching between ubi8 and fedora 33 images while testing.

There is however still the "Invalid argument" problem with storage.conf. Let's fix it.
- The yum install lines below were for the iptables "Invalid argument" that may not be required, therefore commented out.
- The storage.conf "Invalid argument" problem is fixed by commenting out the mountopt line with the arguments.
```
docker volume rm microshift-data;docker volume create microshift-data
docker pull quay.io/microshift/microshift:4.7.0-0.microshift-2021-08-31-224727-aio-linux-arm64
docker run -d --rm --name microshift -h microshift.example.com --privileged -v /lib/modules:/lib/modules -v microshift-data:/var/lib  -p 6443:6443 26adb2be3852 # quay.io/microshift/microshift:4.7.0-0.microshift-2021-08-31-224727-aio-linux-arm64
docker exec -it microshift bash
systemctl stop microshift
systemctl stop crio
#yum -y install http://mirror.centos.org/centos/8/BaseOS/aarch64/os/Packages/conntrack-tools-1.4.4-10.el8.aarch64.rpm http://mirror.centos.org/centos/8/BaseOS/aarch64/os/Packages/libnetfilter_cthelper-1.0.0-15.el8.aarch64.rpm http://mirror.centos.org/centos/8/BaseOS/aarch64/os/Packages/libnetfilter_cttimeout-1.0.0-11.el8.aarch64.rpm http://mirror.centos.org/centos/8/BaseOS/aarch64/os/Packages/libnetfilter_queue-1.0.4-3.el8.aarch64.rpm
#yum -y install https://rpmfind.net/linux/fedora/linux/releases/34/Everything/aarch64/os/Packages/i/iptables-1.8.7-3.fc34.aarch64.rpm https://rpmfind.net/linux/fedora/linux/releases/34/Everything/aarch64/os/Packages/i/iptables-libs-1.8.7-3.fc34.aarch64.rpm https://rpmfind.net/linux/fedora/linux/development/rawhide/Everything/aarch64/os/Packages/g/glibc-2.34.9000-13.fc36.aarch64.rpm https://rpmfind.net/linux/fedora/linux/development/rawhide/Everything/aarch64/os/Packages/g/glibc-common-2.34.9000-13.fc36.aarch64.rpm https://rpmfind.net/linux/fedora/linux/development/rawhide/Everything/aarch64/os/Packages/g/glibc-all-langpacks-2.34.9000-13.fc36.aarch64.rpm https://rpmfind.net/linux/fedora/linux/development/rawhide/Everything/aarch64/os/Packages/g/glibc-minimal-langpack-2.34.9000-13.fc36.aarch64.rpm
sed -i "s/^\(mountopt.*\)/#\\1/" /etc/containers/storage.conf
systemctl stop microshift
systemctl restart crio
systemctl start microshift
```

## Samples to run on Microshift
Run the following within the Microshift container or directly on Jetson Nano if Microshift is installed directly on Jetson.

### 1. Microshift Sample App mysql
Download helm and run the mysql server in a container with hostpath persistent volume and a mysql client container
```
# Install helm
curl -o helm-v3.5.2-linux-arm64.tar.gz  https://get.helm.sh/helm-v3.5.2-linux-arm64.tar.gz
tar -zxvf helm-v3.5.2-linux-arm64.tar.gz
cp linux-arm64/helm /usr/local/bin
chmod 600 /var/lib/microshift/resources/kubeadmin/kubeconfig

# Add the repo for mysql helm chart
helm repo add stable https://charts.helm.sh/stable

# Install mysql with provided image tag (hacky way to use the sha256 tag for the arm64 image) and my-user as the userid with custom passwords for root and my-user
#helm install stable/mysql --generate-name
#helm install mysql stable/mysql --set persistence.enabled=true --set storageClass=kubevirt-hostpath-provisioner --set image=mysql/mysql-server@sha256 --set imageTag=5e373bcea878b3657937c68cdefa8a1504f53e356ac19a3e51bf515e41e0c48c
helm install mysql stable/mysql --set mysqlRootPassword=secretpassword,mysqlUser=my-user,mysqlPassword=my-password,mysqlDatabase=my-database --set persistence.enabled=true --set storageClass=kubevirt-hostpath-provisioner --set image=mysql/mysql-server@sha256 --set imageTag=5e373bcea878b3657937c68cdefa8a1504f53e356ac19a3e51bf515e41e0c48c
helm list

# Remember to delete the /var/hpvolumes/mysql if it already exists (otherwise it will use old password from previous run)
rm -rf /var/hpvolumes/mysql
# Create the persistent volume
kubectl apply -f hostpathpv.yaml

# hostpathpv.yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: hostpath-provisioner
spec:
  #storageClassName: "kubevirt-hostpath-provisioner"
  capacity:
    storage: 8Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/var/hpvolumes/mysql"
...

# Wait for the pod to be Running
kubectl get pods -n default -w

# Start a client container and install the mysql client within it and login using the my-user userid
kubectl run -i --tty ubuntu --image=ubuntu:18.04 --restart=Never -- bash -il
apt-get update && apt-get install mysql-client -y
# replace correct $ipofmysqlserver as seen from few lines below
mysql -h$ipofmysqlserver -umy-user -pmy-password

# You can exec directly into the mysql server and login as root
# If you run the following on the mysql server directly by connecting as root, then you can connect remotely using root too.
cat /etc/hosts # Find the ip of mysql server
mysql -uroot -psecretpassword
update mysql.user set host='%' where user='root';
```

### 2. Microshift Sample App nginx
```
Create the file nginx.yaml

# nginx.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginxinc/nginx-unprivileged:alpine # arm64 image
        ports:
        - containerPort: 8080
        # resource required for hpa
        resources:
          requests:
            memory: 128M
            cpu: 125m
          limits:
            memory: 1024M
            cpu: 1000m
---
apiVersion: v1
kind: Service
metadata:
 name: nginx-svc
 labels:
   app: nginx
spec:
 type: NodePort
 ports:
 - port: 8080
   nodePort: 30080
 selector:
   app: nginx
...

# Create the deployment and service. Test it.
kubectl apply -f nginx.yaml
kubectl get svc # see the port 8080:30080
curl localhost:30080
```

### 3. Microshift Sample Job devicequery
devicequery.yaml
```
apiVersion: batch/v1
kind: Job
metadata:
  name: devicequery-job
spec:
  parallelism: 1
  completions: 1
  activeDeadlineSeconds: 1800
  backoffLimit: 6
  template:
    metadata:
      labels:
        app: devicequery
    spec:
      containers:
      - name: devicequery
        image: docker.io/karve/devicequery:arm64-jetsonnano
      restartPolicy: OnFailure
```
```
oc apply -f devicequery.yaml
```

### 4. Microshift Sample Job vectorAdd
vectoradd.yaml
```
apiVersion: batch/v1
kind: Job
metadata:
  name: vectoradd-job
spec:
  parallelism: 1
  completions: 1
  activeDeadlineSeconds: 1800
  backoffLimit: 6
  template:
    metadata:
      labels:
        app: vectoradd
    spec:
      containers:
      - name: vectoradd
        image: docker.io/karve/vector-add-sample:arm64-jetsonnano
      restartPolicy: OnFailure
```
```
oc apply -f vectoradd.yaml
```

### 5. Microshift Sample Jupyter Lab to access USB camera on /dev/video0
Create the following jupyter.yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jupyter-deployment
spec:
  selector:
    matchLabels:
      app: jupyter
  replicas: 1
  template:
    metadata:
      labels:
        app: jupyter
    spec:
      containers:
      - name: jupyter
        image: nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.6.1
        imagePullPolicy: IfNotPresent
        command: ["/bin/bash", "-c", "jupyter lab --LabApp.token='' --LabApp.password='' --ip 0.0.0.0 --port 8888 --allow-root &> /var/log/jupyter.log && sleep infinity"]
        securityContext:
          privileged: true
          #allowPrivilegeEscalation: false
          #capabilities:
          #  drop: ["ALL"]
        ports:
        - containerPort: 8888
        # resource required for hpa
        resources:
          requests:
            memory: 128M
            cpu: 125m
          limits:
            memory: 2048M
            cpu: 1000m
        volumeMounts:
          - name: dev-video0
            mountPath: /dev/video0
      volumes:
        - name: dev-video0
          hostPath:
            path: /dev/video0

---
apiVersion: v1
kind: Service
metadata:
 name: jupyter-svc
 labels:
   app: jupyter
spec:
 type: NodePort
 ports:
 - port: 8888
   nodePort: 30080
 selector:
   app: jupyter
```
```
oc apply -f jupyter.yaml
```

## Install Metrics Server on Microshift
```
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml -O metrics-server-components.yaml
export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig
kubectl apply -f metrics-server-components.yaml
kubectl get deployment metrics-server -n kube-system
kubectl get events -n kube-system
# Wait for a couple of minutes for metrics to be collected
kubectl top nodes
kubectl top pods -A
```

## Accessing the cluster using API
Reference https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/
```
# Check all possible clusters, as your .KUBECONFIG may have multiple contexts:
kubectl config view -o jsonpath='{"Cluster name\tServer\n"}{range .clusters[*]}{.name}{"\t"}{.cluster.server}{"\n"}{end}'
# Select name of cluster you want to interact with from above output:
export CLUSTER_NAME="some_server_name"
# Point to the API server referring the cluster name
APISERVER=$(kubectl config view -o jsonpath="{.clusters[?(@.name==\"$CLUSTER_NAME\")].cluster.server}")
# It returns multiple tokens, so does not work
TOKEN=$(kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}"|base64 -d)
# Get the token value
kubectl get secrets default-token-g99v6 -o yaml
# Decode it and set the TOKEN
# Explore the API with TOKEN
curl -X GET $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
```

## Questions
- What data does the folder /run/containers/storage/ with userdata contain?
How does it differ from the containers created by cri-o in /var/lib/containers?
- What causes the "Resources before server is ready, possibly a sign for a broken load balancer setup." message in microshift jourtnalctl logs?
https://github.com/redhat-et/microshift/issues/249

## References
- Microshift end to end provisioning demo https://www.youtube.com/watch?v=QOiB8NExtA4
- NVidia GPU Operator on x86-64 with microshift https://gist.github.com/rootfs/2363394bc4f1bd14cf8208ed2ea82038#install-nvidia-gpu-operator
