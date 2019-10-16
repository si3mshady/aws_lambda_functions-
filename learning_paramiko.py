import boto3
import paramiko
import re
import time

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

BUCKET_NAME = 'si3mshady-ssh'
LOG_BUCKET = 'ec2-logs-public'
KEY_NAME = "keyZ.pem"
LOCAL_SCRATCH_SPACE = "/tmp/"
EC2_HOSTNAME =  "ec2-52-23-252-87.compute-1.amazonaws.com"
TARGET_DIR_EC2 = "/home/ubuntu/"
cmd = ['for i in $(sudo find /var/log/ -iname "*log*"); do sudo tar zcf ~/logfiles.$(date +"%Y-%m-%d") $i; done', 'date +"%Y-%m-%d"']

def get_ssh_key_from_s3():
    data = s3.get_object(Bucket=BUCKET_NAME, Key=KEY_NAME)
    ssh_key = data['Body'].read().decode()
    with open(LOCAL_SCRATCH_SPACE + KEY_NAME, 'w') as ink:
        ink.write(ssh_key)
    compress_logs_send_to_s3()

def compress_logs_send_to_s3():
    key = paramiko.RSAKey.from_private_key_file(LOCAL_SCRATCH_SPACE + KEY_NAME)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=EC2_HOSTNAME, username="ubuntu", pkey=key)
    client.exec_command(cmd[0])
    time.sleep(1)
    _, stdout, _ = client.exec_command(cmd[1])
    date_extension = re.sub('\s', "", stdout.read().decode())
    get_compressed_logs_from_ec2(date_extension)

def get_compressed_logs_from_ec2(extension):
    key = paramiko.RSAKey.from_private_key_file(LOCAL_SCRATCH_SPACE + KEY_NAME)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=EC2_HOSTNAME, username="ubuntu", pkey=key)
    ftp = client.open_sftp()
    ftp.get(TARGET_DIR_EC2 + f'logfiles.{extension}', LOCAL_SCRATCH_SPACE + f'/logfiles.{extension}')
    logfile_archive = open(LOCAL_SCRATCH_SPACE + f'/logfiles.{extension}', 'rb')
    send_to_s3(logfile_archive, extension)

def send_to_s3(file,extension):
    response = s3.put_object(ACL='public-read', Body=file, Bucket=LOG_BUCKET, ContentType='application/octet-stream',
                             Key=f'logfiles.{extension}')


get_ssh_key_from_s3()

#EC2 practice with BOTO3; learning PARAMIKO library
#SSH on ec2 instance, create tar compressed archive of all log files, retrieve the files and send to s3
#Elliott Arnold 10-15-19  WIP

#https://aws.amazon.com/blogs/compute/scheduling-ssh-jobs-using-aws-lambda/
#https://medium.com/@keagileageek/paramiko-how-to-ssh-and-file-transfers-with-python-75766179de73