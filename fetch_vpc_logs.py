from datetime import datetime
import boto3
import subprocess
import os


class VPC_LF:

    @classmethod
    def check_inventory_file_exist(cls):
        if  'lf_inventory.txt' not in os.listdir('/home/ubuntu/even_flow'):
            subprocess.check_output([f'touch /home/ubuntu/even_flow/lf_inventory.txt'], shell=True)
        return

    @classmethod
    def begin(cls):
        cls.check_inventory_file_exist()
        if len(cls.check_for_new_log_files()) > 0:
            print('Downloading ' + str(len(cls.check_for_new_log_files())) + ' log files')
            for lf in cls.check_for_new_log_files():
                cls.inventory_log_files_from_s3(lf)
                cls.fetch_vpc_flow_log(lf)
            cls.gunzip()
        else:
            print('No new log files.')

    @classmethod
    def sort_by_date(cls,data):
        '''sort using lambda func - last modified key'''
        return sorted(data, key=lambda x: x['LastModified'])

    @classmethod
    def list_log_files_from_s3(cls):
        bucket_name = 'evenflows'
        s3 = boto3.client('s3')
        return cls.sort_by_date(s3.list_objects(Bucket=bucket_name,
                Marker='AWSLogs/952151691101/vpcflowlogs/us-east-1')['Contents'])

    @classmethod
    def extract_log_file_key_name(cls):
        '''works in tandem with inventory log files from s3'''
        return set([keyname['Key'].split('/')[-1] for keyname in cls.list_log_files_from_s3()])

    @classmethod
    def inventory_log_files_from_s3(cls,logfile):
        '''works in tandem with extract_log_file_key_name'''
        with open('lf_inventory.txt', 'a') as ink:
                ink.write(logfile + '\n')

    @classmethod
    def get_lf_inventory_from_file(cls):
        '''read log file inventory and return set of strings '''
        return set([file.strip() for file in open('lf_inventory.txt').readlines()])

    @classmethod
    def check_for_new_log_files(cls):
        '''check difference in s3 bucket list and local inventory '''
        return cls.extract_log_file_key_name() - cls.get_lf_inventory_from_file()

    @classmethod
    def fetch_vpc_flow_log(cls,lf):
        s3 = boto3.resource('s3')
        formatted_timestring = (datetime.now().strftime('%Y/%m/%d'))
        base_key_path = f'AWSLogs/952151691101/vpcflowlogs/us-east-1/{formatted_timestring}/'
        s3.meta.client.download_file('evenflows', base_key_path + lf, f'/home/ubuntu/even_flow/lf/{lf}')

    @classmethod
    def gunzip(cls,directory='/home/ubuntu/even_flow/lf'):
        '''directory format .../dir../dir   no trailing forward slash for directory '''
        subprocess.check_output([f'gunzip {directory}/*.gz'], shell=True)


VPC_LF.begin()

#AWS EC2 VPC LINUX practice
#Fetching VPC flow logs from s3 to ec2 for future processing
#Elliott Arnold
#elAlquimista
#11-17-19

