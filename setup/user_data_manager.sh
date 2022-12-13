#!/bin/bash
# user data file for cluster management server

# installing required packages
apt update
apt install git dos2unix libaio1 libmecab2 sysbench expect libncurses5 libtinfo5 -y

# fetching config files from git
cd /home/ubuntu
git clone https://github.com/midoxc/8415_Project.git

# installing mysql cluster management server
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
rm mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb

# adding sql cluster config file
mkdir /var/lib/mysql-cluster
dos2unix /home/ubuntu/8415_Project/config.ini
cp /home/ubuntu/8415_Project/config.ini /var/lib/mysql-cluster/

# adding service file
dos2unix /home/ubuntu/8415_Project/ndb_mgmd.service
cp /home/ubuntu/8415_Project/ndb_mgmd.service /etc/systemd/system/

# enabling cluster management on start
systemctl daemon-reload
systemctl enable ndb_mgmd
systemctl start ndb_mgmd

# setup for mysql-server incomplete, see README.md for setup instructions.
# setup for Sakila database incomplete, see README.md for setup instructions.