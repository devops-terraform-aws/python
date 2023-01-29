from flask import Flask, request, render_template
import boto3, botocore

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        instance_id = request.form['instance_id']
        ec2 = boto3.client('ec2', region_name='us-east-1')
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
            result = "Instance terminated successfully"
        except botocore.exceptions.ClientError as e:
            if "InvalidInstanceID.Malformed" in str(e):
                result = "Invalid instance ID"
            else:
                result = "Instance termination not successful: " + str(e)
        return render_template('destroy_index.html', result=result)
    return render_template('destroy_index.html')

if __name__ == '__main__':
    app.run(debug=True)
