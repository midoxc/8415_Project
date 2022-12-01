###
# proxy application to reroute sql requests
###

import paramiko
import random
from flask import Flask, request
from pythonping import ping

app = Flask(__name__)

key = paramiko.RSAKey().from_private_key_file("/home/ubuntu/vockey.pem")

ips = {
    'master'    : 'ip-172-31-1-1.ec2.internal',
    'worker1'   : 'ip-172-31-1-2.ec2.internal', 
    'worker2'   : 'ip-172-31-1-3.ec2.internal', 
    'worker3'   : 'ip-172-31-1-4.ec2.internal'
}

workers = ['worker1','worker2','worker3']

def getLowestPingWorker():
    best = ""
    time = 2000
    for worker in workers:
        ping_result = ping(ips[worker], count=4, timeout=2)
        if ping_result.packet_loss != 4 and time > ping_result.rtt_avg_ms:
            worker = best
            time = ping_result.rtt_avg_ms

    return best

def needsWriteAccess(query):
    instructions = query.split(";")
    for instruction in instructions:
        keyword = instruction.strip().split()[0].lower()
        if keyword in ["delete", "update", "create", "insert", "grant", "revoke"]:
            return True

def formatQuery(query):
    query.replace('"', '\"')
    query.replace('$', '\$')
    query.replace('`', '\`')
    return query

def executeCommands(name, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ips[name], pkey=key, allow_agent=False, look_for_keys=False)
    
    output = ""
    for command in commands:
        print("{} running command: {}".format(name, command))
        stdin , stdout, stderr = ssh.exec_command(command)
        output += "\n" + stdout.read() 
        output += "\n" + stderr.read()

    ssh.close()
    
    return output

def direct(query):   
    return executeCommands("master", ["sudo mysql -u root -e \"{}\"".format(formatQuery(query))])

def randomized(query):
    if not needsWriteAccess(query):
        return executeCommands(random.choice(workers), ["sudo mysql -u root -e \"{}\"".format(formatQuery(query))])

    return direct(query)

def customized(query):
    if not needsWriteAccess(query):
        fastestWorker = getLowestPingWorker()
        if fastestWorker != "":
            return executeCommands(fastestWorker, ["sudo mysql -u root -e \"{}\"".format(formatQuery(query))])

    return direct(query)

# route every POST requests to direct(), regardless of the path (equivalent to a wildcard)
@app.post('/', defaults={'path': ''})
@app.post('/<path:path>')
def handleRequest(path=None):
    type = request.form.get("type")
    query = request.form.get("query")
    
    if type == "custom":
        return customized(query)
    elif type == "random":
        return randomized(query)
    else:
        return direct(query)

if __name__ == '__main__':
      app.run()
