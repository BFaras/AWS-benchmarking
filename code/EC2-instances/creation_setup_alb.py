# Imports
import boto3
from credentials import aws_access_key_id, aws_secret_access_key, aws_session_token, aws_region

# AWS configuration and session setup remains unchanged
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=aws_region
)

# Read instance IDs and security group ID from files
with open('instance_ids.txt', 'r') as f:
    instance_ids = [line.strip() for line in f]

# Split the instances into m4 and t2 types
m4_instance_ids = instance_ids[:5]
t2_instance_ids = instance_ids[5:]

with open('security_group_id.txt', 'r') as f:
    security_group_id = f.read().strip()

# Initialize the ELBv2 client
elbv2_client = session.client('elbv2')

# Create Target Group for m4.large instances
m4_target_group_response = elbv2_client.create_target_group(
    Name='target-group-cluster1',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-0a3368ff043542e23',  # you need to provide your VPC ID here
    TargetType='instance'
)

# Create Target Group for t2.large instances
t2_target_group_response = elbv2_client.create_target_group(
    Name='target-group-cluster2',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-0a3368ff043542e23',  # Update with your VPC ID
    TargetType='instance'
)

# Register m4.large instances with their target group
elbv2_client.register_targets(
    TargetGroupArn=m4_target_group_response['TargetGroups'][0]['TargetGroupArn'],
    Targets=[{'Id': id} for id in m4_instance_ids]
)

# Register t2.large instances with their target group
elbv2_client.register_targets(
    TargetGroupArn=t2_target_group_response['TargetGroups'][0]['TargetGroupArn'],
    Targets=[{'Id': id} for id in t2_instance_ids]
)

# Create Load Balancer
load_balancer_response = elbv2_client.create_load_balancer(
    Name='loadBalancerOne',
    Subnets=['subnet-026b532e2dc93953f', 'subnet-01de3f57035f53fb1'],  # Update with your Subnet IDs
    SecurityGroups=[security_group_id],
    Scheme='internet-facing',
    Type='application'
)

# Create Listener with forwarding rules
listener_response = elbv2_client.create_listener(
    LoadBalancerArn=load_balancer_response['LoadBalancers'][0]['LoadBalancerArn'],
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'ForwardConfig': {
                'TargetGroups': [
                    {
                        'TargetGroupArn': m4_target_group_response['TargetGroups'][0]['TargetGroupArn'],
                        'Weight': 1
                    },
                    {
                        'TargetGroupArn': t2_target_group_response['TargetGroups'][0]['TargetGroupArn'],
                        'Weight': 1
                    }
                ]
            }
        }
    ]
)

# Create Routing Rule for /cluster1
elbv2_client.create_rule(
    ListenerArn=listener_response['Listeners'][0]['ListenerArn'],
    Conditions=[
        {
            'Field': 'path-pattern',
            'Values': ['/cluster1']
        }
    ],
    Priority=1,
    Actions=[
        {
            'Type': 'forward',
            'TargetGroupArn': m4_target_group_response['TargetGroups'][0]['TargetGroupArn']
        }
    ]
)

# Create Routing Rule for /cluster2
elbv2_client.create_rule(
    ListenerArn=listener_response['Listeners'][0]['ListenerArn'],
    Conditions=[
        {
            'Field': 'path-pattern',
            'Values': ['/cluster2']
        }
    ],
    Priority=2,
    Actions=[
        {
            'Type': 'forward',
            'TargetGroupArn': t2_target_group_response['TargetGroups'][0]['TargetGroupArn']
        }
    ]
)

# Save the LoadBalancer ARN
load_balancer_arn = load_balancer_response['LoadBalancers'][0]['LoadBalancerArn']
with open('lb_arn.txt', 'w') as f:
    f.write(load_balancer_arn)

# Save the Target Groups ARNs
m4_target_group_arn = m4_target_group_response['TargetGroups'][0]['TargetGroupArn']
t2_target_group_arn = t2_target_group_response['TargetGroups'][0]['TargetGroupArn']

with open('target_group_arns.txt', 'w') as f:
    f.write(m4_target_group_arn + '\n')
    f.write(t2_target_group_arn + '\n')