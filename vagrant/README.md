# MicroShift in VirtualBox on your Mac

## Run MicroShift in Fedora 35 using Vagrant
```
VAGRANT_VAGRANTFILE=Vagrantfile vagrant up
vagrant ssh
sudo su -
./w.sh # watch the nodes,pods and images
```

## Errors
if your "openshift-service-ca service-ca pod" or "openshift-dns dns-default pod" keep restarting, you may need to reboot the VM, or run the cleanup
```
systemctl stop microshift
crictl rm --all --force
crictl rmp --all --force
sleep 5
crictl rmi --all
pkill -9 conmon
pkill -9 pause
rm -rf /var/lib/microshift
systemctl stop crio
rm -rf /var/lib/containers/*
systemctl start crio
```
Reference
- https://github.com/redhat-et/microshift/issues/270
- https://github.com/redhat-et/microshift/issues/426

## Samples
### Run the mysql with the storageClass=kubevirt-hostpath-provisioner
```
./runme.sh
```

### console
```
./okd-web-console-install.sh
```
Add the 127.0.0.1 console-np-service-kube-system.cluster.local to /etc/hosts on your Mac
http://console-np-service-kube-system.cluster.local

### Node Red with odo
```
./odosample.sh
```
Wait for "Welcome to Node-RED" to appear in the logs

Add the "127.0.0.1 test-app-node-red.cluster.local" to /etc/hosts on your Mac
http://test-app-node-red.cluster.local

## Samples manual install (old docs)
Reference
https://deep75.medium.com/aper%C3%A7u-de-microshift-une-impl%C3%A9mentation-l%C3%A9g%C3%A8re-dopenshift-e60b725849ce

### Installing the OKD Web Console
https://kubevirt.io/2020/OKD-web-console-install.html
```
kubectl create serviceaccount console -n kube-system
kubectl create clusterrolebinding console --clusterrole=cluster-admin --serviceaccount=kube-system:console -n kube-system
kubectl get serviceaccount console --namespace=kube-system -o jsonpath='{.secrets[0].name}' -n kube-system
oc get secret -n $secretnamefromabove -o yaml 
```

Get the openshift.io/token-secret.name from above and replace in yaml below
```
# okd-web-console-install.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: console-deployment
  namespace: kube-system
  labels:
    app: console
spec:
  replicas: 1
  selector:
    matchLabels:
      app: console
  template:
    metadata:
      labels:
        app: console
    spec:
      containers:
        - name: console-app
          image: quay.io/openshift/origin-console:4.2
          env:
            - name: BRIDGE_USER_AUTH
              value: disabled # no authentication required
            - name: BRIDGE_K8S_MODE
              value: off-cluster
            - name: BRIDGE_K8S_MODE_OFF_CLUSTER_ENDPOINT
              value: https://kubernetes.default #master api
            - name: BRIDGE_K8S_MODE_OFF_CLUSTER_SKIP_VERIFY_TLS
              value: "true" # no tls enabled
            - name: BRIDGE_K8S_AUTH
              value: bearer-token
            - name: BRIDGE_K8S_AUTH_BEARER_TOKEN
              valueFrom:
                secretKeyRef:
                  name: console-token-ppfc2 # console serviceaccount token
                  key: token

---
kind: Service
apiVersion: v1
metadata:
  name: console-np-service
  namespace: kube-system
spec:
  selector:
    app: console
  type: NodePort # nodePort configuration
  ports:
    - name: http
      port: 9000
      targetPort: 9000
      nodePort: 30036
      protocol: TCP
...
```
```
kubectl create -f okd-web-console-install.yaml
kubectl get pods,svc -o wide -n kube-system
```
Add the port 30036 to the VirtualBox Microshift VM Settings->Network->Advanced->Port Forwarding
http://localhost:30036

### Get the odo
```
OS="$(uname | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
curl -L https://developers.redhat.com/content-gateway/rest/mirror/pub/openshift-v4/clients/odo/latest/odo-$OS-$ARCH -o odo
sudo install odo /usr/local/bin/
```

### Demo using odo
```
dnf install -y git
git clone https://github.com/deep75/fcdemo3 && cd fcdemo3
odo project create myproject
odo create nodejs
odo push
oc get po,svc -A
curl http://10.43.122.50:3000
oc expose svc -n myproject nodejs-fcdemo3-ysig-app
```
Add the port 80 to the VirtualBox MicroShift VM Settings->Network->Advanced->Port Forwarding

Add the following to /etc/hosts on your Mac
```
127.0.0.0 nodejs-fcdemo3-ysig-app-myproject.cluster.local
```
http://nodejs-fcdemo3-ysig-app-myproject.cluster.local

