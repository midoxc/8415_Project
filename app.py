###
# proxy application to reroute sql requests
###

import paramiko
import random
from flask import Flask, request
from pythonping import ping

app = Flask(__name__)

key = paramiko.RSAKey.from_private_key_file("vockey.pem")

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
        ping_result = ping(ips[worker], count=1, timeout=2)
        if ping_result.packet_loss != 1 and time > ping_result.rtt_avg_ms:
            best = worker
            time = ping_result.rtt_avg_ms

    return best

def needsWriteAccess(query):
    instructions = query.split(";")
    for instruction in instructions:
        keyword = instruction.strip().lower().split()
        if len(keyword) > 0 and keyword[0] in ["delete", "update", "create", "insert", "grant", "revoke"]:
            return True
    return False

def formatQuery(query):
    query = query.replace('"', '\\"')
    query = query.replace('$', '\\$')
    query = query.replace('`', '\\`')
    return query

def executeCommands(name, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ips[name], username="ubuntu", pkey=key, allow_agent=False, look_for_keys=False)

    output = name + "\n"
    for command in commands:
        print("{} running command: {}".format(name, command))
        stdin , stdout, stderr = ssh.exec_command(command)
        out = stdout.read()
        err = stderr.read()
        output += out.decode("latin-1") + "\n"
        output += err.decode("latin-1") + "\n"

    ssh.close()

    return output

def direct(query):
    print("sudo mysql -u root -e \"{}\"".format(formatQuery(query)))
    return executeCommands("master", ["sudo mysql -e \"{}\"".format(formatQuery(query))])

def randomized(query):
    if not needsWriteAccess(query):
        random_worker = random.choice(workers)
        print("read on " + random_worker)
        return executeCommands(random_worker, ["sudo mysql -e \"{}\"".format(formatQuery(query))])

    return direct(query)

def customized(query):
    if not needsWriteAccess(query):
        fastestWorker = getLowestPingWorker()
        if fastestWorker != "":
            print("read on " + fastestWorker)
            return executeCommands(fastestWorker, ["sudo mysql -e \"{}\"".format(formatQuery(query))])

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
    type = str(type).strip()
    query = str(query).strip()

    if type == "custom":
        return customized(query).strip().encode("latin-1")
    elif type == "random":
        return randomized(query).strip().encode("latin-1")
    else:
        return direct(query).strip().encode("latin-1")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
