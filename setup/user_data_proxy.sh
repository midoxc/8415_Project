#!/bin/bash
# user data file for cluster proxy

apt-get update -y
apt-get install python3-venv nginx dos2unix -y

# fetching config files from git
cd /home/ubuntu 
git clone https://github.com/midoxc/8415_Project.git

# adding private ssh key 
echo "-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----" > /home/ubuntu/8415_Project/vockey.pem
chmod 400 /home/ubuntu/8415_Project/vockey.pem

# adding service file
cp /home/ubuntu/8415_Project/proxy.service /etc/systemd/system

# setup python virtual environment
dos2unix /home/ubuntu/8415_Project/requirements.txt
cd /home/ubuntu/8415_Project
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
