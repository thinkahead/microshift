# MicroShift in VirtualBox on your Mac

## Run MicroShift in Fedora 35 using Vagrant
```
vagrant up
vagrant ssh
sudo su -
./w.sh # watch the nodes,pods and images
./runme.sh # Run the mysql with the storageClass=kubevirt-hostpath-provisioner
```

## Samples
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
Expose port 80 on the VirtualBox microshift VM
Add the following to /etc/hosts on your Mac
```
127.0.0.0 nodejs-fcdemo3-ysig-app-myproject.cluster.local
```
http://nodejs-fcdemo3-ysig-app-myproject.cluster.local

