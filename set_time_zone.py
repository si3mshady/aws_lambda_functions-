import boto3, time

class Nsync:
    def __init__(self,instance_id):
        self.instance_id = instance_id
        self.ssm = boto3.client('ssm')
        self.ec2 = boto3.client('ec2')

    def sync(self):
        self.check_instance_ubuntu()
        self.change_tz()

    def check_instance_ubuntu(self):
            try:
                while True:
                    data = self.ec2.get_console_output(InstanceId=self.instance_id)
                    if 'Output' not in data.keys():
                        time.sleep(8)
                        continue
                    if 'ubuntu' in data['Output'].lower():
                        self.assign_ssm_role()
                        break
                    else:
                        pass
            except Exception as e:
                print(e)

    def assign_ssm_role(self):
        self.ec2.associate_iam_instance_profile(
                IamInstanceProfile={'Arn': 'arn:aws:iam::705166095368:instance-profile/SSM_Sandbox',
                                    'Name': 'AmazonSSMFullAccess'}, InstanceId=self.instance_id)
    def change_tz(self):
        try:
            while True:
                self.ssm.send_command(InstanceIds=[self.instance_id], DocumentName='AWS-RunShellScript',
                                      Parameters={'commands': ["sudo timedatectl set-timezone America/Chicago"]})

                print('Command Completed Successfully')

                break
        except Exception as e:
            if "InvalidInstanceId" in str(e):
                time.sleep(8)
                self.change_tz()

def lambda_handler(event,context):
    instance_id = event['detail']['instance-id']
    time_sync = Nsync(instance_id)
    time_sync.sync()

#AWS SSM EC2 Practice - Using Lambda to set timezone on launched instances with SSM
#Quick and Dirty - Use lambda to set the timezone on newly launched instance after confirming OS type is Ubuntu
#2-26-20

















