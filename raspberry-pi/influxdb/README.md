## Influxdb
```
oc newproject influxdb
oc create configmap influxdb-config --from-file=influxdb.conf
oc get configmap influxdb-config -o yaml
oc apply -f influxdb-secrets.yaml
oc describe secret influxdb-secrets
mkdir /var/hpvolumes/influxdb
oc apply -f influxdb-pv.yaml
oc apply -f influxdb-data.yaml
oc apply -f influxdb-deployment.yaml
oc get -f influxdb-deployment.yaml # check that the Deployment is created and ready
oc rsh deployment/influxdb-deployment
```
Output
```
root@ubuntu:~/microshift/raspberry-pi/influxdb# oc rsh deployment/influxdb-deployment
# influx --username admin --password admin
Connected to http://localhost:8086 version 1.7.4
InfluxDB shell version: 1.7.4
Enter an InfluxQL query
> show databases
name: databases
name
----
test
_internal
> exit
# exit
```
```
oc logs deployment/influxdb-deployment -f
oc apply -f influxdb-service.yaml
```

## Telegraf
```
oc apply -f telegraf-config.yaml 
oc apply -f telegraf-secrets.yaml 
oc apply -f telegraf-deployment.yaml
```

Output
```
root@ubuntu:~/microshift/raspberry-pi/influxdb# oc rsh deployment/influxdb-deployment
# influx --username admin --password admin
Connected to http://localhost:8086 version 1.7.4
InfluxDB shell version: 1.7.4
Enter an InfluxQL query
> show databases
name: databases
name
----
test
_internal
telegraf
> use telegraf
Using database telegraf
> show measurements
name: measurements
name
----
cpu
disk
diskio
kernel
mem
net
netstat
processes
swap
system
> select * from cpu;
...
> exit
# exit
```

```
cd grafana
mkdir /var/hpvolumes/grafana
cp -r config/* /var/hpvolumes/grafana/.
oc apply -f grafana-pv.yaml
oc apply -f grafana-data.yaml
oc apply -f grafana-deployment.yaml
oc apply -f grafana-service.yaml
oc expose svc grafana-service # Create the route
```

Add the "RaspberryPiIPAddress grafana-service-influxdb.cluster.local" to /etc/hosts on your laptop and login to http://grafana-service-influxdb.cluster.local using admin/admin. You wll need to change the password on first login.
