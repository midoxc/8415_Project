#!/bin/bash
# user data file for cluster proxy

apt-get update -y
apt-get install python3-venv nginx -y

# fetching config files from git
cd /home/ubuntu 
git clone https://github.com/midoxc/8415_Project.git

# adding private ssh key 
echo "-----BEGIN RSA PRIVATE KEY-----

-----END RSA PRIVATE KEY-----" > /home/ubuntu/8415_Project/vockey.pem

# adding service file
cp /home/ubuntu/8415_Project/proxy.service /etc/systemd/system

# setup python virtual environment
cd /home/ubuntu/8415_Project
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# enabling proxy on start
systemctl daemon-reload
systemctl start proxy
systemctl enable proxy

# enabling nginx service
systemctl start nginx
systemctl enable nginx

# adding nginx config
cp /home/ubuntu/8415_Project/default /etc/nginx/sites-available

# restarting both services to express changes
systemctl restart proxy
systemctl restart nginx
