Install Podman or Docker and build the container image using the Dockerfile.arm64. This will take a few hours to build.
```
apt-get -y install podman
podman build -t docker.io/karve/console:latest -f Dockerfile.arm64 .
podman push docker.io/karve/console:latest
```

For local development, we disable OAuth and run “bridge” with an OpenShift user's access token.
```
oc create serviceaccount console -n kube-system
oc create clusterrolebinding console --clusterrole=cluster-admin --serviceaccount=kube-system:console -n kube-system
oc get serviceaccount console --namespace=kube-system -o jsonpath='{.secrets[0].name}'
```

Replace BRIDGE_K8S_MODE_OFF_CLUSTER_ENDPOINT and secretRef token for BRIDGE_K8S_AUTH_BEARER_TOKEN in okd-web-console-install.yaml
```
oc apply -f okd-web-console-install.yaml
oc expose svc console-np-service -n kube-system
oc get routes -n kube-system
oc logs deployment/console-deployment -f -n kube-system
```
