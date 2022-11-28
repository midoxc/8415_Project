#!/bin/bash
# https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04?fbclid=IwAR1nmdlF3aNVJOOt1S78PGmtf90LlWQ5vFmweb1eOtFMd9G7R-V5u8ko2n4

apt update
apt install git dos2unix libaio1 libmecab2 -y

# fetching files from git
cd ~
git clone https://github.com/midoxc/8415_Project.git

# installing mysql cluster
cd ~
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
rm mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb

# adding sql cluster config file
mkdir /var/lib/mysql-cluster
dos2unix ~/8415_Project/config.ini
cp ~/8415_Project/config.ini /var/lib/mysql-cluster/

# adding service file
dos2unix ~/8415_Project/ndb_mgmd.service
cp ~/8415_Project/ndb_mgmd.service /etc/systemd/system/

rm -r ~/8415_Project

# enabling cluster management on start
systemctl daemon-reload
systemctl enable ndb_mgmd
systemctl start ndb_mgmd

cd ~
cd ~
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar
mkdir install
tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install

# sudo dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
# sudo dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
# sudo dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb
# sudo dpkg -i mysql-cluster-community-server_7.6.6-1ubuntu18.04_amd64.deb

# # root password prompt

# dpkg -i mysql-server_7.6.6-1ubuntu18.04_amd64.deb

# echo "[mysqld]
# # Options for mysqld process:
# ndbcluster                      # run NDB storage engine

# [mysql_cluster]
# # Options for NDB Cluster processes:
# ndb-connectstring=ip-172-31-1-1.ec2.internal  # location of management server" | sudo tee -a /etc/mysql/my.cnf

# sudo systemctl restart mysql
# sudo systemctl enable mysql