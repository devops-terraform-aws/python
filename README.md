# EC2 instance creation using Python and boto3 library
This script allows the user to create an EC2 instance in a specified region using the latest Ubuntu 20.04 LTS AMI. The script uses the `boto3` library to interact with AWS services.

## Prerequisites
- AWS account with permissions to create EC2 instances
- Access key and secret key for the above AWS account
- `boto3` library installed in the Python environment
- A key pair created in the specified region, to allow logging into the EC2 instance.

### To Run in `Browser Mode`
1.  Run the commands:

    `python -m venv venv` <br />
    `source venv/bin/activate` <br />
    `pip install Flask` <br />
    `python -m flask --version` <br />
    `pip install boto3`
    `python app.py`

2. Go to the brower and run

    `localhost:5000`

### To Run on `CLI` or `Locally`
1. Run the commands:

    `python create_ec2.py`

## Usage
1. Run the script using the command `python3 create_ec2.py`
2. The script prompts the user to enter the region they want to create the EC2 instance in (e.g. us-east-1)
3. The script uses the `describe_images` method of the EC2 client to get the latest Ubuntu 20.04 LTS AMI
4. The script then uses the `run_instances` method of the EC2 client to create the EC2 instance, using the specified AMI, instance type, key pair, and security group.
5. The script also attaches a name tag to the instance, for easier identification
6. The script prints the ID of the newly created instance

## Additional notes
- The script uses the owner ID `099720109477`, which belongs to Canonical (the company behind Ubuntu). This is to ensure that only official Ubuntu AMIs are considered
- The script sorts the list of AMIs by the `CreationDate` attribute, in descending order, to ensure that the latest AMI is selected
- The script catches the `IndexError` that is raised when no images are found that match the specified filters and shows the respective message
- The script uses the following paramters for run_instances:
    - `ImageId`: the latest AMI id
    - `InstanceType`: the type of instance to be created. (t2.micro)
    - `MinCount`: minimum number of instances to be created
    - `MaxCount`: maximum number of instances to be created
    - `KeyName`: name of the key pair to be used
    - `SecurityGroups`: name of the security group to be used
    - `TagSpecifications`: add tags to the instance for easy identification.

## Conclusion
This script provides an easy way to spin up an EC2 instance in a specified region, using the latest Ubuntu 20.04 LTS AMI. It can be further modified and integrated into other scripts or automation processes.