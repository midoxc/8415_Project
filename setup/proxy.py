import boto3

ec2_client = boto3.client("ec2", region_name="us-east-1")

# get user data for the proxy instance
user_data_proxy = ""
with open("user_data_proxy.sh", "r") as file:
    user_data_proxy = file.read()

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

def getPublicSecurityGroup():
    """
    Get the public security group if it exists, create it if it doesnt

    :return the public security group
    """
    response = findSecurityGroupsByName('public')

    if len(response['SecurityGroups']) > 0:
        return response['SecurityGroups'][0]
    else:
        public_security_group = ec2_client.create_security_group(
            GroupName='public',
            Description='public-security-group'
        )

        ec2_client.authorize_security_group_ingress(
            CidrIp="0.0.0.0/0",
            IpProtocol='-1',
            FromPort=0,
            ToPort=65535,
            GroupName='public'
        )

        return public_security_group

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
        IamInstanceProfile={
                            'Arn': 'arn:aws:iam::360365674336:instance-profile/LabInstanceProfile'
                     },
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
    # get/create public security group.
    public_security_group = getPublicSecurityGroup()

    # create public proxy instance.
    proxy = createInstance("proxy", "172.31.1.10", public_security_group['GroupId'], user_data_proxy, "t2.large")

    # log proxy instance id.
    print("proxy")
    print(proxy["Instances"][0]["InstanceId"])