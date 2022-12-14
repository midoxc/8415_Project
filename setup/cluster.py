import boto3

ec2_client = boto3.client("ec2", region_name="us-east-1")

# get user data for the master instance
user_data_manager = ""
with open("user_data_manager.sh", "r") as file:
    user_data_manager = file.read()

# get user data for the worker instances
user_data_node = ""
with open("user_data_node.sh", "r") as file:
    user_data_node = file.read()

def findSecurityGroupsByName(name):
    """
    Get the security group if it exists

    :param: name of the security group to find
    :return the security group if it exists
    """
    return ec2_client.describe_security_groups(
        Filters=[
            dict(Name='group-name', Values=[name])
        ]
    )

def getPrivateSecurityGroup():
    """
    Get the private security group if it exists, create it if it doesnt

    :return the private security group
    """
    response = findSecurityGroupsByName('private')

    if len(response['SecurityGroups']) > 0:
        return response['SecurityGroups'][0]
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

        return private_security_group

def createInstance(name, privateIp, SecurityGroupId, userData, InstanceType = "t2.micro"):
    """
    Create an instance from the params passed

    :param: name of the instance to create
    :param: privateIp of the instance to create
    :param: SecurityGroupId of the instance to create
    :param: userData of the instance to create
    :param: InstanceType of the instance to create
    :return the instance created
    """
    return ec2_client.run_instances(
        ImageId="ami-0a6b2839d44d781b2",
        MinCount=1,
        MaxCount=1,
        InstanceType=InstanceType,
        KeyName="vockey",
        UserData=userData,
        SecurityGroupIds=[SecurityGroupId],
        SubnetId='subnet-0d6af2ce628f6f9e2',
        PrivateIpAddress=privateIp,
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': name
                },
            ]
        },
        ]
    )


if __name__ == "__main__":
    # get/create private security group.
    private_security_group = getPrivateSecurityGroup()

    # create cluster instances.
    master = createInstance("master", "172.31.1.1", private_security_group['GroupId'], user_data_manager)
    
    worker1 = createInstance("worker1", "172.31.1.2", private_security_group['GroupId'], user_data_node)

    worker2 = createInstance("worker2", "172.31.1.3", private_security_group['GroupId'], user_data_node)

    worker3 = createInstance("worker3", "172.31.1.4", private_security_group['GroupId'], user_data_node)

    # log master instance id.
    print("master")
    print(master["Instances"][0]["InstanceId"])

    # log workers instance ids.
    print("workers")
    print(worker1["Instances"][0]["InstanceId"])
    print(worker2["Instances"][0]["InstanceId"])
    print(worker3["Instances"][0]["InstanceId"])
