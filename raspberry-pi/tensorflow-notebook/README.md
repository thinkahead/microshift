```
podman build --format docker -t docker.io/karve/tensorflow-notebook:arm64 .
podman push docker.io/karve/tensorflow-notebook:arm64
oc apply -f notebook.yaml
oc -n default wait pod notebook --for condition=Ready --timeout=300s
#oc get pods -w
oc logs notebook -f
```
