#!/bin/bash

apt update
apt install libclass-methodmaker-perl git dos2unix -y

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