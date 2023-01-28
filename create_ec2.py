import boto3

# Prompt the user to enter a region
region = input("Enter the region you want to create the EC2 instance in (e.g. us-east-1): ")

# Create an EC2 client
ec2 = boto3.client('ec2', region_name=region)

# Get the latest Ubuntu 20.04 LTS AMI
response = ec2.describe_images(
    Owners=['099720109477'],
    Filters=[
        {
            'Name':'name',
            'Values':["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
        }])

try:
    response['Images'].sort(key=lambda x: x['CreationDate'], reverse=True)
    ami_id = response['Images'][0]['ImageId']
    #Create an EC2 instance using the latest AMI
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        KeyName='key_2023',
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
    # Print the ID of the newly created instance
    print("Instance created with ID:", response['Instances'][0]['InstanceId'])
except IndexError:
    print("No images found that match the specified filters.")
