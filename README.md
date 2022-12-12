# 8415_Project
Final Project for LOG8415

# setup instuctions
## mysql-server setup instruction for cluster
After running the cluster.py script, run these commands on the master to install mysql-server.
```
cd ~
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
mkdir install
tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

sudo dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb
```
```
sudo dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb
```
*** Note: this package will require the user to enter a password for root. It can be left empty.
```
sudo dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

echo "
[mysqld]
# Options for mysqld process:
ndbcluster                      # run NDB storage engine
bind-address=0.0.0.0            # bind to all available addresses
ndb-connectstring=ip-172-31-1-1.ec2.internal  # location of management server

[mysql_cluster]
# Options for NDB Cluster processes:
ndb-connectstring=ip-172-31-1-1.ec2.internal  # location of management server
" | sudo tee -a /etc/mysql/my.cnf

sudo systemctl restart mysql
sudo systemctl enable mysql
```

## Sakila database setup instruction for cluster
Before setting up Sakila, the previous [mysql-server setup](#mysql-server-setup-instruction-for-cluster) must be completed.

Note that the Sakila database tables will only be present on the master node after the installation since Sakila uses spatial and fulltext indexes.
This means that some tables from Sakila are incompatible with NDB cluster. Therefore, they need to use InnoDB which keeps its data locally in this setup.

Once mysql-server is installed on the master, run these commands to install the Sakila database.
```
cd /home/ubuntu
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvf sakila-db.tar.gz

sudo mysql -u root -e "
SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;
SOURCE /home/ubuntu/sakila-db/sakila-data.sql;
"
```

# benchmarking instructions
To run sysbench tests on the cluster and the standalone server, run these commands on the master instance and the standalone instance respectively.  
## cluster 
### read-write
```
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster prepare
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster --num-threads=6 --max-time=60 --max-requests=0 run
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster cleanup
```
### read-only
```
sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster prepare
sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster --num-threads=6 --max-time=60 --max-requests=0 run
sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster cleanup
```
### write-only
```
sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster prepare
sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster --num-threads=6 --max-time=60 --max-requests=0 run
sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --mysql_storage_engine=ndbcluster cleanup
```

## standalone
### read-write
```
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root prepare
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run
sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root cleanup
```
### read-only
```
sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root prepare
sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run
sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root cleanup
```
### write-only
```
sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root prepare
sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run
sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root cleanup
```

# references
This project was greatly inspired from [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04)
