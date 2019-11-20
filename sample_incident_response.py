from botocore.exceptions import ClientError
from socket import gaierror,herror
import socket
import boto3
import time
import re

class IR:

    @classmethod
    def init(cls):
        data = cls.open_vpc_log()
        for lf in data:
            cls.trigger_incident_response(lf)

    @classmethod
    def open_vpc_log(cls,filename='sample_log_file.txt'):
        try:
            return open(filename).readlines()[1:]
        except FileNotFoundError as e:
            print(e)

    @classmethod
    def trigger_incident_response(cls, string, domain='express.com.ar', target='172.31.84.21'):

        try:
           src, dest = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',string)

           if domain in socket.gethostbyaddr(src)[0] and dest == target:
               instance_id = cls.get_instance_id_from_private_ip(target)

               cls.shut_down_ec2(instance_id)
               volume_id = cls.map_all_instance_id_with_volume_id()[instance_id]
               snapshot_id = cls.create_snapshot(volume_id,instance_id)
               volume_created = False

               while volume_created != True:

                   try:
                     cls.create_volume(snapshot_id)
                     volume_created = True
                   except ClientError:
                       time.sleep(8)

        except (gaierror,herror,ValueError):
            pass

    @classmethod
    def map_all_instance_id_with_volume_id(cls):
            ec2 = boto3.client('ec2')
            volumes = ec2.describe_volumes()

            data_dictionary = {}

            for i in volumes.get('Volumes'):
                try:
                    if i['Attachments'][0]['State'] == 'attached':
                        data_dictionary[i['Attachments'][0]['InstanceId']] = i['Attachments'][0]['VolumeId']
                except IndexError:
                    pass

            return data_dictionary

    @classmethod
    def create_snapshot(cls,volumeId, instance_id):
            client = boto3.client('ec2')

            response = client.create_snapshot(Description='Forensic snapshot for ' + instance_id,
                VolumeId=volumeId,
                DryRun=False)

            return response['SnapshotId']

    @classmethod
    def get_instance_id_from_private_ip(cls,ip):
        ec2 = boto3.client('ec2')
        res = ec2.describe_instances()

        for i in res['Reservations']:
            if ip in i['Instances'][0]['PrivateIpAddress']:
                return i['Instances'][0]['InstanceId']

    @classmethod
    def shut_down_ec2(cls,instance_id):
        ec2 = boto3.client('ec2')
        ec2.stop_instances(InstanceIds=[instance_id],DryRun=False)

    @classmethod
    def create_volume(cls,snapshotId,availibilityZone='us-east-1a'):
            '''create volume from snapshots'''
            client = boto3.client('ec2')
            client.create_volume(
                AvailabilityZone=availibilityZone,
                Encrypted=False,
                SnapshotId=snapshotId,
                VolumeType='gp2',
                DryRun=False)

IR.init()

#AWS Incident Response practice using VPC log data
#Generic IR triggered from rule against source & destionation ips found in VPC log
#When event is triggered -> EC2 instance is stopped, snapshot is taken, and volume is created
#Elliott Arnold
#11-19-19
