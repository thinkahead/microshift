# PostgreSQL Sample with persistence
Create a new project pg. Create the configmap, pv, pvc and deployment for PostgreSQL
```
oc new-project pg
mkdir -p /var/hpvolumes/pg
oc create -f pg-configmap.yaml
oc create -f hostpathpv.yaml
oc create -f hostpathpvc.yaml
oc apply -f pg.yaml
oc get configmap
oc get svc pg-svc
oc get all -lapp=pg
oc logs deployment/pg-deployment -f
```

Output
```
root@raspberrypi:~/microshift/raspberry-pi/pg# oc get all -lapp=pg
NAME                                 READY   STATUS    RESTARTS   AGE
pod/pg-deployment-78cbc9cc88-9rsmk   1/1     Running   0          25s

NAME             TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/pg-svc   NodePort   10.43.13.209   <none>        5432:30080/TCP   25s

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/pg-deployment   1/1     1            1           25s

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/pg-deployment-78cbc9cc88   1         1         1       25s
```

First time we start postgresql, we can check the logs where it creates the database
```
root@raspberrypi:~/microshift/raspberry-pi/pg# oc logs pg-deployment-78cbc9cc88-58mms
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.utf8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

fixing permissions on existing directory /var/lib/postgresql/data ... ok
creating subdirectories ... ok
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default timezone ... Etc/UTC
selecting dynamic shared memory implementation ... posix
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok

Success. You can now start the database server using:

    pg_ctl -D /var/lib/postgresql/data -l logfile start


WARNING: enabling "trust" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or
--auth-local and --auth-host, the next time you run initdb.
waiting for server to start........LOG:  database system was shut down at 2021-12-04 11:44:01 UTC
FATAL:  the database system is starting up
.LOG:  MultiXact member wraparound protections are now enabled
LOG:  autovacuum launcher started
LOG:  database system is ready to accept connections
 done
server started
CREATE DATABASE


/usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*

LOG:  received fast shutdown request
LOG:  aborting any active transactions
LOG:  autovacuum launcher shutting down
waiting for server to shut down....LOG:  shutting down
LOG:  database system is shut down
 done
server stopped

PostgreSQL init process complete; ready for start up.

LOG:  database system was shut down at 2021-12-04 11:44:14 UTC
LOG:  MultiXact member wraparound protections are now enabled
LOG:  autovacuum launcher started
LOG:  database system is ready to accept connections
```
Install the postgresql client
```
apt-get install postgresql-client
```

Connect to the database
```
psql --host localhost --port 30080 --user postgresadmin --dbname postgresdb # test123 as password
```

Create a TABLE cities and insert a couple of rows
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

