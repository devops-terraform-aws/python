from flask import Flask, request, render_template
import boto3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    ami_list = [
        {"ImageId": "ami-00874d747dde814fa", "Name": "Ubuntu Server 22.04 LTS (HVM)"},
        {"ImageId": "ami-0778521d914d23bc1", "Name": "Ubuntu Server 20.04 LTS (HVM)"},
        {"ImageId": "ami-08fdec01f5df9998f", "Name": "Ubuntu Server 18.04 LTS (HVM)"}
    ]
    if request.method == "POST":
        region = request.form["region"]
        tag_name = request.form["tag_name"]
        instance_type = request.form["instance_type"]
        selected_ami = request.form["selected_ami"]
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.run_instances(
                ImageId=selected_ami,
                InstanceType=instance_type,
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
        return render_template("create_index.html", amis=ami_list, response = "Instance created with ID: {}".format(response['Instances'][0]['InstanceId']))
    return render_template("create_index.html", amis=ami_list)


if __name__ == "__main__":
    app.run()
