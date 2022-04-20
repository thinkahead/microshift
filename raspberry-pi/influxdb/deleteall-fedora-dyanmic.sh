oc project influxdb
cd grafana
oc delete route grafana-service
oc delete -f grafana-data.yaml -f grafana-deployment.yaml -f grafana-service.yaml 
cd ..
oc delete -f telegraf-config.yaml -f telegraf-secrets.yaml -f telegraf-deployment.yaml -f measure-deployment-fedora.yaml
oc delete -f influxdb-data.yaml -f influxdb-service.yaml -f influxdb-deployment.yaml -f influxdb-secrets.yaml
sleep 10
oc project default
oc delete project influxdb
