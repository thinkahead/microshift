# Microshift on Jetson Nano
We can run Microshift directly on Ubuntu 18.04 Jetson Nano or within a Docker RHEL8 container on Jetson Nano, the latter is easier. Both options are described. I suggest using the 128GB microSDXC card so that you have sufficient space for experimentation, but Microshift works with the 32GB card.

## Update and Test the Jetson Nano
### Updating your Jetson nano to new Minor Release
Jetson Nano downloads are at https://developer.nvidia.com/embedded/downloads and OS information at https://developer.nvidia.com/embedded/jetpack

If your SD card has older Jetpak, you can update the L4T as follows. The latest is JetPack 4.6 that includes L4T 32.6.1. The platform is t210 for NVIDIA® Jetson Nano™ devices. The version is set to r32.6 (Do not set to r32.6.1)
```
vi /etc/apt/sources.list.d/nvidia-l4t-apt-source.list

deb https://repo.download.nvidia.com/jetson/common r32.6 main
deb https://repo.download.nvidia.com/jetson/t210 r32.6 main

apt update
apt dist-upgrade
# If your hostname is without a domain, you may want to add the ".example.com"
# There was an issue on microshift saying that this is required
# I don't think adding the domain is necessary anymore, but might as well do it
hostnamectl set-hostname jetson-nano.example.com # replace jetson-nano with your short hostname
dpkg-reconfigure tzdata # Select your timezone
```

### DLI "Getting Started with AI on Jetson Nano" Course Environment Container
https://ngc.nvidia.com/catalog/containers/nvidia:dli:dli-nano-ai
```
docker run --runtime nvidia -it --rm --network host --volume ~/nvdli-data:/nvdli-nano/data --device /dev/video0 nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.6.1
```
Connect to your Jetson nano ip address and login with pasword dlinano [http://192.168.1.205:8888/lab?](http://192.168.1.205:8888/lab?)

## Install dependencies and build Microshift binary for arm64 on Ubuntu 18.04 - Jetson Nano
You may either copy the microshift binary from the docker image I have created for the jetson nano or build it.

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

### Testing cri-o with nginx (optional)
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
crictl create $podid nginx.json net-pod.json # The container for nginx will go into Created state
crictl ps -a # List containers, get the containerid
crictl start $containerid # Go to Running state
crictl logs $containerid
crictl stop $containerid # Go to Exited state
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
ExecStart=microshift run
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

sed -i 's|^ExecStart=microshift|ExecStart=/usr/local/bin/microshift|' /usr/lib/systemd/system/microshift.service
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

### Errors
#### The node was low on resource: [DiskPressure]
If you have less than 10% free disk space on the microSDXC card, the kubevirt-hostpath-provisioner pod may get evicted. This will happen on the 32GB microSDXC card if the disk space cannot be reclaimed after deleting usused images. You will need to create space by deleting some github sources we had downloaded for installation.
```
rm -rf /root/.cache/go-build # Cleanup to get space on microSDXC card
# You can check the eviction events as follows
kubectl describe nodes
kubectl get events --field-selector involvedObject.kind=Node
kubectl delete events --field-selector involvedObject.kind=Node
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
```

## Running Microshift in docker container on Ubuntu 18.04 - Jetson Nano
On jetson-nano (if you installed firewalld previously, ignore otherwise):
```
firewall-cmd --zone=public --permanent --add-port=9443/tcp
firewall-cmd --reload
```

Build microshift binary as mentioned in previous section. You will copy the microshift binary for creating the image. The arm64 images and microshift binaries within images from https://quay.io/repository/microshift/microshift?tab=tags did not work in Docker on Jetson Nano. I got the error with iptables with the quay.io/microshift/microshift:4.7.0-0.microshift-2021-08-31-224727-aio-linux-arm64 when the container was started and the pods within the microshift container stayed in ContainerCreating state:
```
Oct 07 14:38:21 microshift.example.com microshift[78]: E1007 14:38:21.128486      78 proxier.go:874] Failed to ensure that filter chain KUBE-EXTERNAL-SERVICES exists: error creating chain "KUBE-EXTERNAL-SERVICES": exit status 4: iptables v1.8.4 (nf_tables): Could not fetch rule set generation id: Invalid argument

Oct 07 14:38:22 microshift.example.com microshift[78]: W1007 14:38:22.321539      78 iptables.go:564] Could not set up iptables canary mangle/KUBE-PROXY-CANARY: error creating chain "KUBE-PROXY-CANARY": exit status 4: iptables v1.8.4 (nf_tables): Could not fetch rule set generation id: Invalid argument
```

### Build the Microshift docker image on Jetson Nano
Build the microshift image on your Jetson Nano. You may skip this if you pulled the docker image earlier.
```
systemctl start docker
git clone https://github.com/thinkahead/microshift.git
cd microshift/hack/all-in-one
cp /root/microshift/microshift . # copy the microshift binary built earlier to this folder
# HOST=xxx below should not be rhel8, so I just set it to ubuntu18
docker build --build-arg HOST=ubuntu18 -t microshift .
```

### Start the microshift container and exec into it
```
docker run -d --rm --name microshift -h microshift.example.com --privileged -v /lib/modules:/lib/modules -v microshift-data:/var/lib -p 9443:6443 microshift # or use the docker.io/karve/microshift:arm64-jetsonnano
docker exec -it microshift bash
export KUBECONFIG=/var/lib/microshift/resources/kubeadmin/kubeconfig 
watch "kubectl get nodes;kubectl get pods -A;crictl images;crictl pods" # wait for 2 minutes

# The openshift-ingress and openshift-dns keep restarting, lets fix it.
systemctl stop microshift
crictl rm --all --force
crictl rmp --all --force
crictl rmi --all
pkill -9 conmon
pkill -9 pause
rm -rf /var/lib/microshift
systemctl start microshift
```

## Samples to run on Microshift
Run the following within the Microshift container or directly on Jetson Nano if Microshift is installed directly on Jetson.

### Sample mysql
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

### Sample nginx
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

## Links
Microshift end to end provisioning demo https://www.youtube.com/watch?v=QOiB8NExtA4

