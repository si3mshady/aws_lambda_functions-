import boto3
import re
import time


class Rescue911:

    def __init__(self,instance_id):
        self.ec2R = boto3.resource('ec2')
        self.ec2C = boto3.client('ec2')
        self.emergency_pattern = "(Kernel panic)([\s\S]{67})"
        self.instance_id = instance_id
        self.detached_volume_id = self.get_effected_volume_id()
        self.rescue_instance_id = None
        self.az = self.get_az()

    def get_console_output(self):
        ec2instance = self.ec2R.Instance(self.instance_id)
        return ec2instance.console_output()['Output']

    def check_kernel_panic(self):
        if len(re.findall(self.emergency_pattern,self.get_console_output())) > 0:
            self.stop_effected_ec2()
            self.check_instance_stopped()
            self.detach_volume()
            self.launch_rescue_instance()
            self.check_instance_running()
            self.attach_volume()
               #initiate rescue sequence

    def describe_instances(self):
        #map instance id and instance current state
        return {status['Instances'][0]['InstanceId']: status['Instances'][0]['State'] \
                  for status in self.ec2C.describe_instances()['Reservations']}


    def check_instance_stopped(self):
        while True:
            if self.describe_instances()[self.instance_id]['Name'] == 'stopped':
                break
            else:
                time.sleep(8)


    def check_instance_running(self):
        while True:
            if self.describe_instances()[self.rescue_instance_id]['Name'] == 'running':
                break
        else:
            time.sleep(8)

    def get_ami_type(self):
        ec2instance = self.ec2R.Instance(self.instance_id)
        return ec2instance.image_id

    def stop_effected_ec2(self):
        self.ec2C.stop_instances(InstanceIds=[self.instance_id],Force=True)


    def get_effected_volume_id(self):
        #map instance_ids with volume_id
        volumes = self.ec2C.describe_volumes()
        data_dictionary = {}
        for i in volumes.get('Volumes'):
            try:
                if i['Attachments'][0]['State'] == 'attached':
                    data_dictionary[i['Attachments'][0]['InstanceId']] = i['Attachments'][0]['VolumeId']
            except IndexError:
                pass
        return data_dictionary[self.instance_id]

    def get_az(self):
        #instance and volume must be in the same AZ
        return {az['Instances'][0]['InstanceId']: az['Instances'][0]['Placement']['AvailabilityZone'] \
                  for az in  self.ec2C.describe_instances()['Reservations']}[self.instance_id]


    def get_effected_device(self):
        volumes = self.ec2C.describe_volumes()
        data_dictionary = {}
        for i in volumes.get('Volumes'):
            try:
                if i['Attachments'][0]['State'] == 'attached':
                    data_dictionary[i['Attachments'][0]['VolumeId']] = i['Attachments'][0]['Device']
            except IndexError:
                pass
        return data_dictionary[self.get_effected_volume_id()]


    def launch_rescue_instance(self):
        response = self.ec2C.run_instances(
            ImageId=self.get_ami_type(),
            InstanceType='t2.medium',
            KeyName='acloudGuru',
            MinCount=1,
            MaxCount=1,
            Placement={'AvailabilityZone': self.az}
        )

        self.rescue_instance_id = response['Instances'][0]['InstanceId']

    def detach_volume(self):
        self.ec2C.detach_volume(
            Device=self.get_effected_device(),
            Force=True,
            InstanceId=self.instance_id,
            VolumeId=self.detached_volume_id,
            DryRun=False
        )


    def attach_volume(self):
        self.ec2C.attach_volume(
            Device='/dev/xvdf',
            InstanceId=self.rescue_instance_id,
            VolumeId=self.detached_volume_id,
            DryRun=False
        )


def lambda_handler(event,context):
    instance_id = event['detail']['instance-id']
    r911 = Rescue911(instance_id)
    r911.check_kernel_panic()



#AWS Troubleshooting Practice - Collaboration w/ Mike Z
# Use EC2 console log output to detect issues with system booting.
# Lambda provides events for all ec2 state changes
# If a configured event i.e "Kernel Panic" is detected in the console log output
# the EBS volume is  detached from the downed instance and attach to EC2 rescue image
# to continue troubleshooting on a working EC2 instance.
# Kernel Panic simulation by modifying initramfs under /boot/
#Elliott Arnold
#1-11-2020


