import paramiko
import boto3

class MountFS:
    def __init__(self,instance_id):
        self.SSH_KEY_LOC = "/tmp/keyZ.pem"
        self.MOUNT_SCRIPT_LOC = "/tmp/autoMount.py"
        self.instance_id = instance_id
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')

    def init_mount(self):
        self.download_script()
        self.download_ssh_key()
        self.ssh_put_script()
        self.ssh_run_command()

    def get_dns_name(self):
        response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        return response['Reservations'][0]['Instances'][0]['PublicDnsName']

    def download_ssh_key(self,bucket='ssh-keyz',key='keyZ.pem'):
        s3_resp = self.s3.get_object(Bucket=bucket, Key=key)
        ssh_key = s3_resp['Body'].read().decode()
        with open(self.SSH_KEY_LOC,'w') as ink:
            ink.write(ssh_key)

    def download_script(self, bucket='ssh-keyz', key='autoMount.py'):
        s3_resp = self.s3.get_object(Bucket=bucket, Key=key)
        mount_script = s3_resp['Body'].read().decode()
        with open(self.MOUNT_SCRIPT_LOC, 'w') as ink:
            ink.write(mount_script)
        print('Script downloaded')

    def ssh_put_script(self):
        key = paramiko.RSAKey.from_private_key_file(self.SSH_KEY_LOC)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.get_dns_name(), username="ubuntu", pkey=key)
        ftp = client.open_sftp()
        ftp.put(self.MOUNT_SCRIPT_LOC,'/home/ubuntu/autoMount.py')
        ftp.close()
        print('Script Uploaded')

    def ssh_run_command(self):
        key = paramiko.RSAKey.from_private_key_file(self.SSH_KEY_LOC)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.get_dns_name(), username="ubuntu", pkey=key)
        _, stdout, _ = client.exec_command('python3  /home/ubuntu/autoMount.py')
        print('Command Run Successfully')


def lambda_handler(event,context):
    instance_id = event['detail']['responseElements']['instanceId']
    mount = MountFS(instance_id)
    mount.init_mount()
