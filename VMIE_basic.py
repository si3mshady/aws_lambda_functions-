import boto3
import json


class VMIE:
    def __init__(self, event):
        self.event = event
        self.ec2 = boto3.client('ec2')
        self.ssm = boto3.client('ssm')
        self.ami_name = None
        self.volume_size = None
        self.vm_role = self.ssm.get_parameter(Name='vmie-role-name')['Parameter']['Value']
        # establish default document structure
        self.default_params = {"Architecture": 'x86_64', "ClientData": {'Comment': '', "UploadSize": None},
                               "Description": '', "DiskContainers": [{'UserBucket': {'S3Bucket': '', 'S3Key': ''}}, ],
                               "Hypervisor": 'xen', "Platform": 'Linux', "RoleName": self.vm_role}

    def process_vm_import(self):
        # parse main event - using sns the message body is in str format, use json loads to convert into dictionary
        filename = json.loads(self.event['Records'][0]['Sns']['Message'])['Records'][0]['s3']['object']['key']
        size = int(json.loads(self.event['Records'][0]['Sns']['Message'])['Records'][0]['s3']['object']['size'] / 1000000)
        bucket = json.loads(self.event['Records'][0]['Sns']['Message'])['Records'][0]['s3']['bucket']['name']
        # prepare new values with keys found in default document
        attributes = {}
        attributes['ClientData'] = {'Comment': filename.split('.')[0], "UploadSize": size}
        attributes['Description'] = filename.split('.')[0] + ' img'
        attributes['DiskContainers'] = [{'UserBucket': {'S3Key': filename, 'S3Bucket': bucket}}]
        # import image  (kwargs x 2)
        self.import_vm(**self.set_vm_attributes(**attributes))
        # pass values to parameter store for later use, set default attributes
        self.ami_name = 'ami-' + filename.split('.')[0]
        self.volume_size = size
        self.ssm.put_parameter(Name="new-ami-name", Value=self.ami_name.split('.ova')[0], Type='String')
        self.ssm.put_parameter(Name="volume-size", Value=str(self.volume_size), Type='String')

    def set_vm_attributes(self, **kwargs):
        # dynamically replace default values with new values for matching keys
        for key, val in kwargs.items():
            self.default_params[key] = val
        return self.default_params

    def import_vm(self, **kwargs):
        self.ec2.import_image(**kwargs)

    def create_ami_from_snapshot(self, snapshot_id):
        # get values from parameter store 
        self.ami_name = self.ssm.get_parameter(Name='new-ami-name')['Parameter']['Value']
        self.volume_size = int(self.ssm.get_parameter(Name='volume-size')['Parameter']['Value'])

        attrs = {'Name': self.ami_name, 'RootDeviceName': '/dev/sda1',
                 'VirtualizationType': 'hvm', 'BlockDeviceMappings': [{'DeviceName': '/dev/sda1',
                 'Ebs': {'DeleteOnTermination': True,'SnapshotId': snapshot_id,
                 'VolumeSize': self.volume_size,'VolumeType': 'gp2'}}]}

        result = self.ec2.register_image(**attrs)
        self.ssm.put_parameter(Name="ami-image-id", Value=result['ImageId'], Type='String')


def lambda_handler(event, context):
    print(event)
    try:
        if 'ObjectCreated:' in json.loads(event['Records'][0]['Sns']['Message'])['Records'][0]['eventName']:
            vmie = VMIE(event)
            vmie.process_vm_import()
    except KeyError:
        try:
            if 'copySnapshot' == json.loads(event['Records'][0]['Sns']['Message'])['detail']['event'] \
                    and json.loads(event['Records'][0]['Sns']['Message'])['detail']['result'] == 'succeeded':
                snapshot_id = json.loads(event['Records'][0]['Sns']['Message'])['resources'][0].split('/')[-1]
                vmie = VMIE(event)
                vmie.create_ami_from_snapshot(snapshot_id)
        except KeyError:
            pass

# AWS SNS Lambda VirtualMachineImportExport VMIE practice
# Migrate on-prem VM to AWS - S3 and Cloudwatch events trigger lambda workflow
# Upload OVF, create import task, generate snapshot, and register AMI
# WIP Covid19_quarantine
# Elliott Arnold  4-4-20 


