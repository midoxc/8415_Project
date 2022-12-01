###
# proxy application to reroute sql requests
###
import requests
import paramiko
from flask import Flask

app = Flask(__name__)

master_ip = ['ip-172-31-1-1.ec2.internal']
worker_ips = ['ip-172-31-1-2.ec2.internal', 'ip-172-31-1-3.ec2.internal', 'ip-172-31-1-4.ec2.internal']

# route every requests to hello(), regardless of the path (equivalent to a wildcard)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path = None):
    return 'hi'

if __name__ == '__main__':
      app.run()
