import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
key_name = 'aem'
response = ec2.run_instances(
    ImageId='ami-0ff8a91507f77f867',
    InstanceType='t2.micro',         
    MinCount=1,                      
    MaxCount=1,                       
    KeyName=key_name,
    SecurityGroups=['default'],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'python-EC2'
                },
            ]
        },
    ]

)

instance_id = response['Instances'][0]['InstanceId']
print(f'Instance ID: {instance_id}')
