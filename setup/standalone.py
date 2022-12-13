import boto3

# get user data for standalone instance
user_data_standalone = ""
with open("user_data_standalone.sh", "r") as file:
    user_data_standalone = file.read()

if __name__ == "__main__":
    ec2_client = boto3.client("ec2", region_name="us-east-1")

    # get public security group if it exists
    response = ec2_client.describe_security_groups(
        Filters=[
            dict(Name='group-name', Values=['public'])
        ]
    )
    
    public_security_group = ''
    if len(response['SecurityGroups']) > 0:
        public_security_group = response['SecurityGroups'][0]
    else:
        # if public security group does not exist, create it.
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

    # create standalone instance.
    standalone = ec2_client.run_instances(
        ImageId="ami-0ee23bfc74a881de5",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="vockey",
        UserData=user_data_standalone,
        SecurityGroupIds=[public_security_group['GroupId']],
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'standalone'
                },
            ]
        },
        ]
    )

    # log standalone instance id.
    print("standalone")
    print(standalone["Instances"][0]["InstanceId"])
