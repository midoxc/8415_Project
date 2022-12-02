import requests
import boto3
import sys

ec2_client = boto3.client("ec2", region_name="us-east-1")

def getInstancesByName(name):
    response = ec2_client.describe_instances(
        Filters=[{
    'Name':'tag:Name',
    'Values': [name]},
    {
    'Name':'instance-state-name',
    'Values': ['running', 'stopped', 'stopping', 'rebooting', 'pending']}]
    )
    return response["Reservations"][0]["Instances"]

def isInstanceRunning(id):
    response = ec2_client.describe_instance_status(InstanceIds=[id], IncludeAllInstances=True)
    return response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'

def sendQuery(url, type, query):
    return requests.post(url,json={"type": type, "query": query})

if __name__ == "__main__":
    instances = getInstancesByName("proxy")
    if len(instances) == 0:
        print("Proxy does not exist. Please create and run it.")
        exit(1)
    
    proxy = instances[0]

    if not isInstanceRunning(proxy["InstanceId"]):
        print("Proxy is not running. Please start it and/or wait for it to run.")
        exit(1)

    type = ""
    if len(sys.argv) == 1:
        print("choose a proxy type:")
        print("-- (1) direct - default")
        print("-- (2) random")
        print("-- (3) custom")
        type = input(">>> ")

    if len(sys.argv) > 1:
        type = sys.argv[1]

    if type in ["2", "random"]:
        type = "random"
    elif type in ["3", "custom"]:
        type = "custom"
    else:
        type = "direct"

    if len(sys.argv) < 3:
        text = ""
        while True:
            line = input("> ")
            text += line + "\n"
            if len(line) > 0 and line[-1] == ";":
                response = sendQuery("http://" + proxy["PublicDnsName"], type, text)
                print(response.content.decode("latin-1"))
                text = ""
                
            if line.lower().count("exit") > 0:
                break

    if len(sys.argv) == 3:
        with open(sys.argv[2]) as file:
            response = sendQuery("http://" + proxy["PublicDnsName"], type, file.read())
            print(response.content.decode("latin-1"))

