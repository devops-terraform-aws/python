import boto3

region = input("Enter the region you want to search for AMIs in (e.g. us-east-1): ")
ec2 = boto3.client('ec2', region_name=region)

response = ec2.describe_images(
    Owners=['099720109477'],
    Filters=[
        {
            'Name':'name',
            'Values':["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]}])

response['Images'].sort(key=lambda x: x['CreationDate'], reverse=True)

most_recent_ami = response['Images'][0]

print(most_recent_ami['ImageId'])