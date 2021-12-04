# Postgresql Sample with persistence
Create a new project pg, configmpa, pv, pvc and deployment
```
oc new-project pg
mkdir -p /var/hpvolumes/pg
oc create -f pg-configmap.yaml
oc create -f hostpathpv.yaml
oc create -f hostpathpvc.yaml
oc apply -f pg.yaml
oc get configmap
oc get svc pg-svc
```

Install the postgresql client
```
apt-get install postgresql-client
```

Connect to the database
```
psql --host localhost --port 30080 --user postgresadmin --dbname postgresdb # test123 as password
```

Create a TABLE cities and insert a coupkle of rows
```
CREATE TABLE cities (name varchar(80), location point);
\t
INSERT INTO cities VALUES ('Madison', '(89.40, 43.07)'),('San Francisco', '(-122.43,37.78)');
SELECT * from cities;
\d
\q
```

Let's delete the deployment and recreate it
```
oc delete -f .
```

Check that the data still exists
```
root@raspberrypi:~/microshift/raspberry-pi/pg# ls /var/hpvolumes/pg/data/
base	 pg_commit_ts  pg_ident.conf  pg_notify    pg_snapshots  pg_subtrans  PG_VERSION	    postgresql.conf
global	 pg_dynshmem   pg_logical     pg_replslot  pg_stat	 pg_tblspc    pg_xlog		    postmaster.opts
pg_clog  pg_hba.conf   pg_multixact   pg_serial    pg_stat_tmp	 pg_twophase  postgresql.auto.conf
```

Let's recreate the deployment and look at the deployment logs. This time it already has a database.
```
oc create -f .
oc logs deployment/pg-deployment -f
```

```
PostgreSQL Database directory appears to contain a database; Skipping initialization

LOG:  database system was shut down at 2021-12-04 12:11:13 UTC
LOG:  MultiXact member wraparound protections are now enabled
LOG:  autovacuum launcher started
LOG:  database system is ready to accept connections
```

Now we can connect to the database and look at the cities table
```
psql --host localhost --port 30080 --user postgresadmin --dbname postgresdb # test123 as password
SELECT * FROM cities;
\q
```

Output
```
psql (13.5 (Debian 13.5-0+deb11u1), server 9.6.24)
Type "help" for help.

postgresdb=# SELECT * FROM cities;
     name      |    location
---------------+-----------------
 Madison       | (89.4,43.07)
 San Francisco | (-122.43,37.78)
(2 rows)
```

