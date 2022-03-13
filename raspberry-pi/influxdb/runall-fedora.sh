#!/bin/bash
shopt -s expand_aliases
alias oc="oc --insecure-skip-tls-verify"
oc new-project influxdb

# InfluxDB
oc create configmap influxdb-config --from-file=influxdb.conf
oc apply -f influxdb-secrets.yaml
#mkdir /var/hpvolumes/influxdb # This will get created with the persistent volume
#ssh -p 22222 root@mydevice.local mkdir /mnt/data/hpvolumes/influxdb
oc apply -f influxdb-pv.yaml
oc apply -f influxdb-data.yaml
while [[ $(kubectl get pvc influxdb-data -o 'jsonpath={..status.phase}') != "Bound" ]]; do echo "waiting for PVC status" && sleep 1; done
oc apply -f influxdb-deployment.yaml -f influxdb-service.yaml
oc wait -f influxdb-deployment.yaml --for condition=available

# SenseHat Measurements
oc apply -f measure-deployment-fedora.yaml
oc wait -f measure-deployment-fedora.yaml --for condition=available

# Telegraf
oc apply -f telegraf-config.yaml -f telegraf-secrets.yaml -f telegraf-deployment.yaml
oc wait -f telegraf-deployment.yaml --for condition=available

cd grafana
mkdir /var/hpvolumes/grafana
cp -r config/* /var/hpvolumes/grafana/.
oc apply -f grafana-pv.yaml
oc apply -f grafana-data.yaml
while [[ $(kubectl get pvc grafana-data -o 'jsonpath={..status.phase}') != "Bound" ]]; do echo "waiting for PVC status" && sleep 1; done
oc apply -f grafana-deployment.yaml -f grafana-service.yaml
oc wait -f grafana-deployment.yaml --for condition=available
oc expose svc grafana-service # Create the route
cd ..

oc get route grafana-service
