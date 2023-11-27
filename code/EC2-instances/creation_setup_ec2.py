# Imports
import boto3
from credentials import aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region

# AWS CLI configuration values
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=aws_region
)

# Initialize the EC2 client
ec2_client = session.client('ec2')

# Define Security Group details
security_group_name = 'test'
security_group_description = 'Security Group Description'

# Create Security Group
security_group_response = ec2_client.create_security_group(
    GroupName=security_group_name,
    Description=security_group_description,
)

security_group_id = security_group_response['GroupId']

# Authorize Security Group Ingress for SSH and HTTP
ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    CidrIp='0.0.0.0/0'
)

ec2_client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=80,
    ToPort=80,
    CidrIp='0.0.0.0/0'
)

# Launch m4.large EC2 instances
m4_instance_response = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    InstanceType='m4.large',
    MinCount=5,
    MaxCount=5,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName='vockey',
    SecurityGroups=[security_group_name]
)

# Launch t2.large EC2 instances
t2_instance_response = ec2_client.run_instances(
    ImageId='ami-053b0d53c279acc90',
    InstanceType='t2.large',
    MinCount=4,
    MaxCount=4,
    Placement={'AvailabilityZone': 'us-east-1b'},
    KeyName='vockey',
    SecurityGroups=[security_group_name]
)

# Extract instance IDs and save to a file
instance_ids = [instance['InstanceId'] for instance in m4_instance_response['Instances']]
instance_ids.extend([instance['InstanceId'] for instance in t2_instance_response['Instances']])

with open('instance_ids.txt', 'w') as f:
    for instance_id in instance_ids:
        f.write(instance_id + '\n')

# Save the created security group id to a file for future reference
with open('security_group_id.txt', 'w') as f:
    f.write(security_group_id)
