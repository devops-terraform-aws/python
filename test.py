from flask import Flask, request, render_template
import boto3
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def index():
    ec2 = boto3.client('ec2', region_name='us-west-2')
    regions = ec2.describe_regions()['Regions']
    return render_template('index.html', regions=regions)

@app.route('/amis', methods=['POST'])
@cache.cached(timeout=3600)
def amis():
    region = request.form['region']
    ec2 = boto3.client('ec2', region_name=region)
    images = ec2.describe_images(Owners=['amazon'], Filters=[
        {'Name': 'architecture', 'Values': ['x86_64']},
        {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-*']}
    ])['Images']
    amis = [image['Name'] for image in images[:3]]
    return render_template('amis.html', amis=amis)

if __name__ == '__main__':
    app.run(debug=True)




# from flask import Flask, request, render_template
# import boto3
# from flask_caching import Cache

# app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# @app.route('/')
# def index():
#     ec2 = boto3.client('ec2', region_name='us-west-2')
#     regions = ec2.describe_regions()['Regions']
#     return render_template('index.html', regions=regions)

# @app.route('/amis', methods=['POST'])
# @cache.cached(timeout=3600)
# def amis():
#     region = request.form['region']
#     ec2 = boto3.client('ec2', region_name=region)
#     images = ec2.describe_images(Owners=['amazon'], Filters=[{'Name': 'architecture', 'Values': ['x86_64']}])['Images']
#     amis = [image['Name'] for image in images[:3]]
#     return render_template('amis.html', amis=amis)

# if __name__ == '__main__':
#     app.run(debug=True)
