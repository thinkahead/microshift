# nginx sample with template
First we will run a nginx sample using a template. This uses the image docker.io/nginxinc/nginx-unprivileged:alpine
```
oc project default # If you use a different namespace xxxx, you will need to change the /etc/hosts to match the nginx-xxxx.cluster.local accordingly
#oc process -f nginx-template-deploymentconfig.yml | oc apply -f - # deploymentconfig does not work in microshift
oc process -f nginx-template-deployment-8080.yml | oc apply -f - # deployment works in microshift
oc get templates
oc get routes
```
Add the following to /etc/hosts on the Raspberry Pi 4
```
127.0.0.1 localhost nginx-default.cluster.local
```

Then run
```
curl nginx-default.cluster.local
```

To delete
```
oc process -f nginx-template-deployment-8080.yml | oc delete -f -
```

Other commands
```
# Either of the following two may be used:
oc create -f nginx-template-deployment-8080.yml
#oc create -f nginx-template-deployment-80.yml

oc process nginx-template | oc apply -f -
curl nginx-default.cluster.local
oc process nginx-template | oc delete -f -
oc delete template nginx-template
```

# nginx sample
Create the data in /var/hpvolumes/nginx/data1. The data1 is because we use the subPath in the volumeMounts in the nginx.yaml
```
mkdir -p /var/hpvolumes/nginx/data1/
cp index.html /var/hpvolumes/nginx/data1/.
cp 50x.html /var/hpvolumes/nginx/data1/.
```
This will create the pv, pvc, deployment and service. There will be two replicas sharing the same persistent volume.
```
oc apply -f hostpathpvc.yaml
oc apply -f hostpathpv.yaml
oc apply -f nginx-privileged.yaml
oc apply -f nginx.yaml
```
Give a request as follows:
```
oc get pods # replace the pod name below with either of the nginx pod names
oc exec -it nginx-deployment-7b4d76f8d8-vjgzt -- cat /usr/share/nginx/html/index.html
curl localhost:30080
```

Change the replicas
```
oc scale deployment.v1.apps/nginx-deployment --replicas=1
```

We can delete the deployment and service
```
oc delete -f nginx.yaml
```

Then delete the pvc
```
oc delete hostpathpvc.yaml
```

Now if we want to reuse the pv, we have to delete the claimRef from the pv
```
kubectl edit pv hostpath-provisioner
# Delete the complete claimRef field and save
oc apply -f hostpathpvc.yaml # create a new claim, it will work now
oc apply -f nginx.yaml # create the nginx again
```
