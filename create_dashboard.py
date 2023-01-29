from flask import Flask, request, render_template
import boto3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        region = request.form["region"]
        tag_name = request.form["tag_name"]
        ec2 = boto3.client('ec2', region_name=region)
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
                                'Value': tag_name
                            },
                        ]
                    },
                ]
            )
            return render_template("create_index.html", response = "Instance created with ID: {}".format(response['Instances'][0]['InstanceId']))
        except IndexError:
            return render_template("create_index.html", response = "No images found that match the specified filters.")
    else:
        return render_template("create_index.html")

if __name__ == "__main__":
    app.run()
