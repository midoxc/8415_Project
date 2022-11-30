#!/bin/bash

# install mysql
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

# #read-write
# sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root prepare
# sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run
# sudo sysbench oltp_read_write --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root cleanup

# #read-only
# sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root prepare
# sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run
# sudo sysbench oltp_read_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root cleanup

# #write-only
# sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root prepare
# sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root --num-threads=6 --max-time=60 --max-requests=0 run
# sudo sysbench oltp_write_only --table-size=100000 --db-driver=mysql --mysql-db=sakila --mysql-user=root cleanup
