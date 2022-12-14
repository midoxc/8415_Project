#!/bin/bash
# user data file for cluster data nodes

# installing required packages
apt update
apt install libclass-methodmaker-perl git dos2unix expect libaio1 libmecab2  -y

# fetching config files from git
cd /home/ubuntu
git clone https://github.com/midoxc/8415_Project.git

# installing mysql cluster data node
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
rm mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

# adding sql cluster node config file
dos2unix /home/ubuntu/8415_Project/my.cnf
cp /home/ubuntu/8415_Project/my.cnf /etc/

# creating sql cluster node data folder
mkdir -p /usr/local/mysql/data

# adding service file
dos2unix /home/ubuntu/8415_Project/ndbd.service
cp /home/ubuntu/8415_Project/ndbd.service /etc/systemd/system/

# enabling cluster management on start
systemctl daemon-reload
systemctl enable ndbd
systemctl start ndbd