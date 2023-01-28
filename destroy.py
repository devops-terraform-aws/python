import boto3
instance_id = input("Enter instance_id: ")

ec2 = boto3.client('ec2', region_name='us-east-1')
ec2.terminate_instances(InstanceIds=[instance_id])
