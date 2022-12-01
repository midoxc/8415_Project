#!/bin/bash
# user data file for standalone mysql server

apt-get update
apt-get install mysql-server sysbench -y

cd ~
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xvf sakila-db.tar.gz
rm sakila-db.tar.gz

mysql -u root -e "
SOURCE ~/sakila-db/sakila-schema.sql;
SOURCE ~/sakila-db/sakila-data.sql;
"

rm ~/sakila-db.tar.gz