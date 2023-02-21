import io
from flask import Flask, request, render_template, send_file
import boto3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    ami_list = [
        {"ImageId": "ami-00874d747dde814fa", "Name": "Ubuntu Server 22.04 LTS (HVM)"},
        {"ImageId": "ami-0778521d914d23bc1", "Name": "Ubuntu Server 20.04 LTS (HVM)"},
        {"ImageId": "ami-08fdec01f5df9998f", "Name": "Ubuntu Server 18.04 LTS (HVM)"},
        {"ImageId": "ami-0dfcb1ef8550277af", "Name": "Amazon Linux 2 AMI (HVM)"}
    ]
    if request.method == "POST":
        region = request.form["region"]
        tag_name = request.form["tag_name"]
        instance_type = request.form["instance_type"]
        selected_ami = request.form["selected_ami"]
        create_key = request.form.get("create_key")
        key_name = request.form.get("key_name")
        download_key = request.form.get("download_key")
        if create_key:
            ec2 = boto3.client('ec2', region_name=region)
            key_pair = ec2.create_key_pair(KeyName=key_name)
            with open(key_name + '.pem', 'w') as f:
                f.write(key_pair['KeyMaterial'])
            key_data = io.StringIO(key_pair['KeyMaterial']).read().encode('utf-8')
            if download_key:
                return send_file(io.BytesIO(key_data), as_attachment=True, download_name=key_name+'.pem')
            else:
                return "Key created successfully"
        else:
            ec2 = boto3.client('ec2', region_name=region)
            response = ec2.run_instances(
                    ImageId=selected_ami,
                    InstanceType=instance_type,
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
                                    'Value': tag_name
                                },
                            ]
                        },
                    ]
                )
            return render_template("create_index.html", amis=ami_list, response="Instance created with ID: {}".format(response['Instances'][0]['InstanceId']))
    return render_template("create_index.html", amis=ami_list)


if __name__ == "__main__":
    app.run()
