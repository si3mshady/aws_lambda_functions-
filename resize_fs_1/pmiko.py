import paramiko
import boto3

class UseParamiko:
    def __init__(self,instance_id):
        self.SSH_KEY_LOC = "/tmp/testing.pem"
        self.SCRIPT_LOC = "/tmp/extend_file_system.py"
        self.instance_id = instance_id
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')

    def init(self):
        self.download_script()
        self.download_ssh_key()
        self.ssh_put_script()
        self.ssh_run_command()

    def get_dns_name(self):
        response = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        return response['Reservations'][0]['Instances'][0]['PublicDnsName']

    def download_ssh_key(self,bucket='extend-fs',key='testing.pem'):
        s3_resp = self.s3.get_object(Bucket=bucket, Key=key)
        ssh_key = s3_resp['Body'].read().decode()
        with open(self.SSH_KEY_LOC,'w') as ink:
            ink.write(ssh_key)
        print('Ssh key downloaded')

    def download_script(self, bucket='extend-fs', key='extend_file_system.py'):
        s3_resp = self.s3.get_object(Bucket=bucket, Key=key)
        mount_script = s3_resp['Body'].read().decode()
        with open(self.SCRIPT_LOC, 'w') as ink:
            ink.write(mount_script)
        print('Script downloaded')

    def ssh_put_script(self):
        key = paramiko.RSAKey.from_private_key_file(self.SSH_KEY_LOC)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.get_dns_name(), username="ec2-user", pkey=key)
        ftp = client.open_sftp()
        ftp.put(self.SCRIPT_LOC,'/home/ec2-user/extend_file_system.py')
        ftp.close()
        print('Script Uploaded')

    def ssh_run_command(self):
        key = paramiko.RSAKey.from_private_key_file(self.SSH_KEY_LOC)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.get_dns_name(), username="ec2-user", pkey=key)
        _, stdout, _ = client.exec_command('python3  /home/ec2-user/extend_file_system.py')
        print('Command Run Successfully')

#AWS Lambda Cloudwatch EBS Alarm Simulation
#Increase root ebs volume size and filesystem upon low storage condition
#Elliott Arnold
#12-5-19