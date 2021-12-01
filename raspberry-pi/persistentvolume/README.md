# nginx sample
Create the data in /var/hpvolumes/nginx/data1
```
mkdir -p /var/hpvolumes/nginx/data1/
cp index.html /var/hpvolumes/nginx/data1/.
cp 50x.html /var/hpvolumes/nginx/data1/.
```
This will create the pv, pvc, deployment and service. There will be two replicas sharing the same persistent volume.
```
oc apply -f .
```
Give a request as follows:
```
oc get pods # replace the pod name below with eithewr of your pod names
oc exec -it nginx-deployment-7b4d76f8d8-vjgzt -- cat /usr/share/nginx/html/index.html
curl localhost:30080
```

You can delete the deployment and service
```
oc delete -f nginx.yaml
```

Then  delete the pvc
```
oc delete hostpathpvc.yaml
```

Now if you want to reuse the pv
```
kubectl edit pv hostpath-provisioner
# Delete rthe complete claimRef field and save
oc apply -f hostpathpvc.yaml
```
