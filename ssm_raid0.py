import boto3,re,time

class ConfigureRaid0:
    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.ec2 = boto3.client('ec2')
        self.ssm = boto3.client('ssm')
        self.label = f'RAID0_{self.instance_id}'
        self.raid_commands = self.prepare_raid_commands()

    def assign__ssm_iam_role(self):
        self.ec2.associate_iam_instance_profile(
            IamInstanceProfile={'Arn': 'arn:aws:iam::705166095368:instance-profile/SSM_Sandbox','Name': 'AmazonSSMFullAccess' },
            InstanceId=self.instance_id)

    def run_commands_ssm(self):
        for cmd in self.raid_commands:
            self.ssm.send_command(InstanceIds=[self.instance_id],DocumentName='AWS-RunShellScript',
            Parameters={'commands': [cmd]})
            time.sleep(3)

    def get_device_name(self):
        #get EBS device names as detected on target instance
        data = self.ec2.describe_instances(InstanceIds=[self.instance_id])
        device_names = [dn['DeviceName'] \
            for dn in data['Reservations'][0]['Instances'][0]['BlockDeviceMappings'] \
                if dn['DeviceName'] !='/dev/xvda']
        device_names = [re.sub('s', 'xv', dev) for dev in device_names]
        return device_names

    def prepare_raid_commands(self):
        cmd_list = []
        dev_names = self.get_device_name()
        num_devices = len(dev_names)
        raid0_cmd = f"sudo mdadm --create --verbose /dev/md0 --level=0 \
         --name={self.label} --raid-devices={num_devices} {dev_names[0]} {dev_names[1]}"
        cmd_list.append(raid0_cmd)
        make_ext4_fs =   f"sudo mkfs.ext4 -L {self.label} /dev/md0 | at now + 5 minutes"
        cmd_list.append(make_ext4_fs)
        create_mdadm_conf = 'sudo mdadm --detail --scan | sudo tee -a /etc/mdadm.conf | at now + 6 minutes'
        cmd_list.append(create_mdadm_conf)
        create_initramfs = 'sudo dracut -H -f /boot/initramfs-$(uname -r).img $(uname -r) | at now + 7 minutes'
        cmd_list.append(create_initramfs)
        mkdir = "sudo mkdir -p /mnt/raid  | at now + 8 minutes"
        cmd_list.append(mkdir)
        mount = f'sudo mount LABEL={self.label} /mnt/raid | at now + 9 minutes'
        cmd_list.append(mount)
        back_up_fstab = f'sudo cp /etc/fstab /etc/fstab.orig  | at now + 9 minutes'
        cmd_list.append(back_up_fstab)
        amend_fstab = f"sudo echo {self.label}    /mnt/raid   ext4    defaults,nofail      0       2 >> /etc/fstab | at now + 10 minutes"
        cmd_list.append(amend_fstab)
        return cmd_list


def lambda_handler(event, context):
    instance_id = event['detail']['responseElements']['instanceId']
    config = ConfigureRaid0(instance_id)
    config.assign__ssm_iam_role()
    config.run_commands_ssm()

#AWS SSM LAMBDA LINUX practice
#Execute commands on managed EC2 instances using ssm
#Configure EBS volumes with Raid0 for increased iops preformance
#Elliott Arnold  2-1-20
#https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/raid-config.html

