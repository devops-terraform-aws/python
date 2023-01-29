import boto3, botocore

ec2 = boto3.client('ec2', region_name='us-east-1')

valid = False
while not valid:
    instance_id = input("Enter instance_id: ")
    try:
        ec2.terminate_instances(InstanceIds=[instance_id])
        print("Instance terminated successfully")
        valid = True
    except botocore.exceptions.ClientError as e:
        if "InvalidInstanceID.Malformed" in str(e):
            print("Invalid instance ID, please try again.")
        else:
            print("Instance termination not successful:", e)
            valid = True

