#!/bin/bash
#shopt -s expand_aliases
#alias oc="oc --insecure-skip-tls-verify"
oc new-project influxdb

# InfluxDB
oc create configmap influxdb-config --from-file=influxdb.conf
oc apply -f influxdb-secrets.yaml
#mkdir /var/hpvolumes/influxdb # This will get created with the persistent volume
#ssh -p 22222 root@mydevice.local mkdir /mnt/data/hpvolumes/influxdb
#oc apply -f influxdb-pv.yaml -f influxdb-data.yaml
oc apply -f influxdb-data-dynamic.yaml
while [[ $(kubectl get pvc influxdb-data -o 'jsonpath={..status.phase}') != "Bound" ]]; do echo "waiting for PVC status" && sleep 1; done
oc apply -f influxdb-deployment.yaml -f influxdb-service.yaml
oc wait -f influxdb-deployment.yaml --for condition=available --timeout=2m

# SenseHat Measurements
oc apply -f measure-deployment-fedora.yaml
oc wait -f measure-deployment-fedora.yaml --for condition=available --timeout=2m

# Telegraf
oc apply -f telegraf-config.yaml -f telegraf-secrets.yaml -f telegraf-deployment.yaml
oc wait -f telegraf-deployment.yaml --for condition=available

cd grafana
#oc apply -f grafana-pv.yaml -f grafana-data.yaml
#grafanadir=/var/hpvolumes/grafana
#mkdir $grafanadir
oc apply -f grafana-data-dynamic.yaml
while [[ $(kubectl get pvc grafana-data -o 'jsonpath={..status.phase}') != "Bound" ]]; do echo "waiting for PVC status" && sleep 1; done
grafanadir=`oc get pvc grafana-data | grep grafana-data | awk '{print $3}'`
cp -r config/* /var/hpvolumes/$grafanadir/.
oc apply -f grafana-deployment.yaml -f grafana-service.yaml
oc wait -f grafana-deployment.yaml --for condition=available --timeout=2m
oc expose svc grafana-service # Create the route
cd ..

oc get route grafana-service
