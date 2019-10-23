import boto3

class Snapshots:
    def get_ec2_instanceIds_and_availibilityZones(self):
        client = boto3.client('ec2')
        instances = client.describe_instances()
        return {id['Instances'][0]['InstanceId']: id['Instances'][0]['Placement']['AvailabilityZone'] for id in
                instances.get('Reservations')}

    # create instance_id to volume_id mapping
    def map_all_instance_id_with_volume_id(self):
        client = boto3.client('ec2')
        volumes = client.describe_volumes()
        data_dictionary = {}
        for i in volumes.get('Volumes'):
            try:
                if i['Attachments'][0]['State'] == 'attached':
                    data_dictionary[i['Attachments'][0]['InstanceId']] = i['Attachments'][0]['VolumeId']
            except IndexError:
                pass
        return data_dictionary

    # tag and instance/ resources
    def create_tag(self,resource_list, key, value):
        '''resource_list,key,value'''
        ec2_resource = boto3.resource('ec2')
        response = ec2_resource.create_tags(
            DryRun=False,
            Resources=resource_list,
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )
        return response

    def match_tag_with_volume_id_instance_id(self,key):
        '''param key for desired tag'''
        client = boto3.client('ec2')
        volumes = client.describe_volumes()
        for i in volumes.get("Volumes"):
            try:
                if key in i['Tags'][0].values():
                    print('Instance_id:', i['Attachments'][0]['InstanceId'])
                    print('Volume_id:', i['Attachments'][0]['VolumeId'])
            except:
                pass

    def create_snapshot(self,description, volumeId):
        '''params description & volume id  '''
        client = boto3.client('ec2')
        response = client.create_snapshot(
            Description=description,
            VolumeId=volumeId,
            DryRun=False
        )

        return response

    def create_volume(self,availibilityZone, snapshotId):
        '''create volume from snapshots'''
        client = boto3.client('ec2')
        response = client.create_volume(
            AvailabilityZone=availibilityZone,
            Encrypted=False,
            SnapshotId=snapshotId,
            VolumeType='gp2',
            DryRun=False
        )

        return response

    def attach_volume(self,disk, instanceId, volumeId):
        client = boto3.client('ec2')
        response = client.attach_volume(
            Device=f'/dev/{disk}',
            InstanceId=instanceId,
            VolumeId=volumeId,
            DryRun=False
        )

        return response

    def detach_volume(self,disk, instanceId, volumeId):
        client = boto3.client('ec2')
        response = client.attach_volume(
            Device=f'/dev/{disk}',
            Force=True,
            InstanceId=instanceId,
            VolumeId=volumeId,
            DryRun=False
        )
        return response



#AWS EBS | Snapshot (backup/restore) practice
#Created a small class with utility functions to create backups and restore them on to EC2 instances
#Elliott Arnold 10-23-19
#si3mshady

#https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html




