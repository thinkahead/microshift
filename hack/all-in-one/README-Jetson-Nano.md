# Containerized Microshift 

On jetson-nano:
```
firewall-cmd --zone=public --permanent --add-port=9443/tcp
firewall-cmd --reload
```

Build microshift binary. The arm64 images and microshift binaries within images from https://quay.io/repository/microshift/microshift?tab=tags did not work in Docker on Jetson Nano. I got the error with iptables with the quay.io/microshift/microshift:4.7.0-0.microshift-2021-08-31-224727-aio-linux-arm64 when the container was started and the pods within the microshift container stayed in ContainerCreating state:
```
Oct 07 14:38:21 microshift.example.com microshift[78]: E1007 14:38:21.128486      78 proxier.go:874] Failed to ensure that filter chain KUBE-EXTERNAL-SERVICES exists: error creating chain "KUBE-EXTERNAL-SERVICES": exit status 4: iptables v1.8.4 (nf_tables): Could not fetch rule set generation id: Invalid argument

Oct 07 14:38:22 microshift.example.com microshift[78]: W1007 14:38:22.321539      78 iptables.go:564] Could not set up iptables canary mangle/KUBE-PROXY-CANARY: error creating chain "KUBE-PROXY-CANARY": exit status 4: iptables v1.8.4 (nf_tables): Could not fetch rule set generation id: Invalid argument
```

Build the microshift image on Jetson Nano
```
git clone https://github.com/thinkahead/microshift.git
cd microshift/hack/all-in-one
# HOST=xxx below should not be rhel8, so I just set it to ubuntu18
docker build --build-arg HOST=ubuntu18 -t microshift .
```

We start the microshift container and exec into it
```
docker run -d --rm --name microshift -h microshift.example.com --privileged -v /lib/modules:/lib/modules -v microshift-data:/var/lib  -p 9443:6443 microshift
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

Still in the microshift container, download helm and run the mysql server in a container with hostpath persistent volume and a mysql client container
```
# Install helm
curl -o helm-v3.5.2-linux-arm64.tar.gz  https://get.helm.sh/helm-v3.5.2-linux-arm64.tar.gz
tar -zxvf helm-v3.5.2-linux-arm64.tar.gz
cp linux-arm64/helm /usr/local/bin
chmod 600 /var/lib/microshift/resources/kubeadmin/kubeconfig

# Add the repo for mysql helm chart
helm repo add stable https://charts.helm.sh/stable

# Install mysql with provided image tag (hacky way to use the sha256) and my-user as the userid with custom passwords for root and my-user
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

Another example with nginx
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
        image: nginxinc/nginx-unprivileged:alpine
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

Accessing the cluster using API https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/
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

