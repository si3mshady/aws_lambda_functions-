from pmiko import UseParamiko
import boto3
import re

def lambda_handler(event, context):
    data = event['Records'][0]['Sns']['Message']
    instance_id = re.findall("(i-[a-z0-9]*)", data)[0]
    print(instance_id)
    modify = ModVolume(instance_id)
    modify.modVolume()

class ModVolume:

    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.ec2_client = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')

    def modVolume(self):
        volume_id = self.get_volume_id(self.instance_id)
        self.modify_volume(volume_id)
        extend_fs = UseParamiko(self.instance_id)
        extend_fs.init()

    def get_volume_id(self, instance_id):
        results = self.map_all_instance_id_with_volume_id()
        volume_id = results[instance_id]
        return volume_id

    def get_current_volume_size(self, volume_id):
        volume = self.ec2_resource.Volume(volume_id)
        return volume.size

    def modify_volume(self, volume_id):
        response = self.ec2_client.modify_volume(
            DryRun=False,
            VolumeId=volume_id,
            Size=self.get_current_volume_size(volume_id) + 50,
            VolumeType='gp2'
        )
        return response

    def map_all_instance_id_with_volume_id(self):

        volumes = self.ec2_client.describe_volumes()
        data_dictionary = {}
        for i in volumes.get('Volumes'):
            try:
                if i['Attachments'][0]['State'] == 'attached':
                    data_dictionary[i['Attachments'][0]['InstanceId']] = i['Attachments'][0]['VolumeId']
            except IndexError:
                pass
        return data_dictionary

#AWS Lambda Cloudwatch EBS Alarm Simulation
#Increase root ebs volume size and filesystem upon low storage condition
#Elliott Arnold
#12-5-19