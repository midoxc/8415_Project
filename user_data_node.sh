#!/bin/bash

apt update
apt install libclass-methodmaker-perl git dos2unix expect libaio1 libmecab2 -y

cd ~
git clone https://github.com/midoxc/8415_Project.git
cd ~
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
rm mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

dos2unix ~/8415_Project/my.cnf
cp ~/8415_Project/my.cnf /etc/

mkdir -p /usr/local/mysql/data

dos2unix ~/8415_Project/ndbd.service
cp ~/8415_Project/ndbd.service /etc/systemd/system/

rm -r ~/8415_Project

systemctl daemon-reload
systemctl enable ndbd
systemctl start ndbd

cd ~
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
mkdir install
tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

sudo dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb
#sudo dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb

cp ~/8415_Project/script.exp ~/install/
chmod +x ./script.exp
./script.exp

dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

echo "
[mysqld]
# Options for mysqld process:
ndbcluster                      # run NDB storage engine
ndb-connectstring=ip-172-31-1-1.ec2.internal  # location of management server

[mysql_cluster]
# Options for NDB Cluster processes:
ndb-connectstring=ip-172-31-1-1.ec2.internal  # location of management server
" | sudo tee -a /etc/mysql/my.cnf

sudo systemctl restart mysql
sudo systemctl enable mysql

cd ~
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvf sakila-db.tar.gz

rm -r ~/8415_Project

sudo mysql -u root -e "
SOURCE ~/sakila-db/sakila-schema.sql;
SOURCE ~/sakila-db/sakila-data.sql;
"