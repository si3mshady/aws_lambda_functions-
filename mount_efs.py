import boto3
import time
import paramiko


class MountEfS:
    def __init__(self,instance_id):
        self.ec2 = boto3.client('ec2')
        self.instance_id = instance_id
        self.s3 = boto3.client('s3')

    def check_instance_tagged(self):
        results = self.ec2.describe_instances()

        #use of 'get' method will not throw exception error out if key is absent, rather provides a default value of None
        instanceId_tag_mapping =  {i['Instances'][0]['InstanceId']: i['Instances'][0].get('Tags') \
                                   for i in  results['Reservations']}

        if instanceId_tag_mapping[self.instance_id] == None:
            self.mount_efs()
            self.tag_instance()
        else:
            pass

    def get_dns_name(self):
        response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        return response['Reservations'][0]['Instances'][0]['PublicDnsName']

    def download_ssh_key(self, bucket='efs-sandbox', key='acloudGuru.pem'):
        s3_resp = self.s3.get_object(Bucket=bucket, Key=key)
        ssh_key = s3_resp['Body'].read().decode()
        with open('/tmp/acg.pem', 'w') as ink:
            ink.write(ssh_key)

    def mount_efs(self):
        self.download_ssh_key()
        key = paramiko.RSAKey.from_private_key_file('/tmp/acg.pem')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.get_dns_name(), username="ec2-user", pkey=key)

        #install nfs, create directory and mount EFS in new instance
        commands = ["sudo yum install -y nfs-utils","mkdir /home/ec2-user/efs",
        "sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-c1292740.efs.us-east-1.amazonaws.com:/ /home/ec2-user/efs"]

        for cmd in commands:
            _, stdout, _ = client.exec_command(cmd)
            time.sleep(8)
            client.connect(hostname=self.get_dns_name(), username="ec2-user", pkey=key)

        print('Commands Run Successfully.')

    def tag_instance(self):
        self.ec2.create_tags(
            DryRun=False,
            Resources=[
               self.instance_id
            ],
            Tags=[
                {
                    'Key': 'efs',
                    'Value': 'mounted'
                },
            ]
        )

def lambda_handler(event,context):
    instance_id = event['detail']['instance-id']
    mefs = MountEfS(instance_id)
    mefs.check_instance_tagged()

#AWS EFS Cloudwatch practice = Using Cloudwatch and Lambda to mount Elastic File Systems (EFS) on new instances as they are launched - quick and dirty
#Elliott Arnold
#1-5-20