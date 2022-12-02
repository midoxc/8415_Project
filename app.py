###
# proxy application to reroute sql requests
###

import paramiko
import random
from flask import Flask, request
from pythonping import ping
import os

app = Flask(__name__)

key = paramiko.RSAKey.from_private_key_file("vockey.pem")

ips = {
    'master'    : 'ubuntu@ip-172-31-1-1.ec2.internal',
    'worker1'   : 'ubuntu@ip-172-31-1-2.ec2.internal',
    'worker2'   : 'ubuntu@ip-172-31-1-3.ec2.internal',
    'worker3'   : 'ubuntu@ip-172-31-1-4.ec2.internal'
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
        out = stdout.read()
        err = stderr.read()
        print(os.popen("echo " + out).read())
        print(err)
        output += out.decode("ISO-8859-1") + "\n"
        output += err.decode("ISO-8859-1") + "\n"

    ssh.close()

    return output

def direct(query):
    print("sudo mysql -u root -e \"{}\"".format(formatQuery(query)))
    return executeCommands("master", ["sudo mysql -u root -e \"{}\"".format(formatQuery(query))])

def randomized(query):
    if not needsWriteAccess(query):
        return executeCommands(random.choice(workers), ["sudo mysql -u root -e \"{}\"".format(formatQu$

    return direct(query)

def customized(query):
    if not needsWriteAccess(query):
        fastestWorker = getLowestPingWorker()
        if fastestWorker != "":
            return executeCommands(fastestWorker, ["sudo mysql -u root -e \"{}\"".format(formatQuery(q$

    return direct(query)

# route every POST requests to direct(), regardless of the path (equivalent to a wildcard)
@app.post('/', defaults={'path': ''})
@app.post('/<path:path>')
def handleRequest(path=None):
    type = request.json.get("type")
    query = request.json.get("query")

    if str(type) == "" or str(query) == "":
        return "INVALID POST PARAMS : missing type or query \n" + request.json

    print(request.json)
    type = str(type)
    query = str(query)
    print()
    if type == "custom":
        return customized(query)
    elif type == "random":
        return randomized(query)
    else:
        return direct(query)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
