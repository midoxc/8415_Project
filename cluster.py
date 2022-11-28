import boto3
import time

user_data_manager = ""
user_data_node = ""

with open("user_data_manager.sh", "r") as file:
    user_data_manager = file.read()

with open("user_data_node.sh", "r") as file:
    user_data_node = file.read()

def check_instances_running(instancesId):
    response = ec2_client.describe_instance_status(InstanceIds=[master['Instances'][0]['InstanceId']], IncludeAllInstances=True)
    for statuses in response['InstanceStatuses']:
        if statuses['InstanceState']['Name'] != 'running':
            return False
    return True

def get_public_ip(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))

if __name__ == "__main__":
    ec2_client = boto3.client("ec2", region_name="us-east-1")

    response = ec2_client.describe_security_groups(
        Filters=[
            dict(Name='group-name', Values=['private'])
        ]
    )
    
    private_security_group = ''
    if len(response['SecurityGroups']) > 0:
        private_security_group = response['SecurityGroups'][0]
    else:
        private_security_group = ec2_client.create_security_group(
            GroupName='private',
            Description='private-security-group'
        )

        ec2_client.authorize_security_group_ingress(
            CidrIp="172.31.0.0/20",
            IpProtocol='-1',
            FromPort=0,
            ToPort=65535,
            GroupName='private'
        )

        ec2_client.authorize_security_group_ingress(
            CidrIp="0.0.0.0/0",
            IpProtocol='tcp',
            FromPort=22,
            ToPort=22,
            GroupName='private'
        )


    master = ec2_client.run_instances(
        ImageId="ami-0ee23bfc74a881de5",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=user_data_manager,
        SecurityGroupIds=[private_security_group['GroupId']],
        SubnetId='subnet-0d6af2ce628f6f9e2',
        PrivateIpAddress="172.31.1.1",
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'master'
                },
            ]
        },
        ]
    )
    
    worker1 = ec2_client.run_instances(
        ImageId="ami-0ee23bfc74a881de5",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=user_data_node,
        SecurityGroupIds=[private_security_group['GroupId']],
        SubnetId='subnet-0d6af2ce628f6f9e2',
        PrivateIpAddress="172.31.1.2",
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'worker1'
                },
            ]
        },
        ]
    )
    worker2 = ec2_client.run_instances(
        ImageId="ami-0ee23bfc74a881de5",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=user_data_node,
        SecurityGroupIds=[private_security_group['GroupId']],
        SubnetId='subnet-0d6af2ce628f6f9e2',
        PrivateIpAddress="172.31.1.3",
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'worker2'
                },
            ]
        },
        ]
    )
    worker3 = ec2_client.run_instances(
        ImageId="ami-0ee23bfc74a881de5",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=user_data_node,
        SecurityGroupIds=[private_security_group['GroupId']],
        SubnetId='subnet-0d6af2ce628f6f9e2',
        PrivateIpAddress="172.31.1.4",
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'worker3'
                },
            ]
        },
        ]
    )

    print("master")
    print(master["Instances"][0]["InstanceId"])

    print("workers")
    print(worker1["Instances"][0]["InstanceId"])
    print(worker2["Instances"][0]["InstanceId"])
    print(worker3["Instances"][0]["InstanceId"])
