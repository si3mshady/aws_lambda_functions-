import boto3, paramiko


class DefaultEC2:
    
    def __init__(self):
        self.ec2 = boto3.resource('ec2')

    def create_security_group(self,group_name):
        '''returns tuple security group_id, group_name'''
        self.base_sg_params = {"Description": "For Testing Purposes", "GroupName": group_name}
        self.group = self.ec2.create_security_group(**self.base_sg_params)
        return (self.group.id, group_name)

    def add_basic_ssh_rule_to_securityGroup( self, group_id, group_name):
        '''default ssh group permissions'''
        ingress_premissions = [
            {

                'FromPort': 22,
                'IpProtocol': 'tcp',

                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': group_name + " created with py script"
                    },
                ],

                'ToPort': 22
            }
        ]
        self.authorize_inbound_rule(group_id=group_id,group_name=group_name,permissions_list=ingress_premissions)

    def authorize_inbound_rule(self, group_id, group_name, permissions_list):
        '''params group id, group name, ip permissions'''
        self.security_group = self.ec2.SecurityGroup(group_id)
        resp = self.security_group.authorize_ingress(GroupName=group_name, IpPermissions=permissions_list)

    def getDefaultEC2Params(security_group_id):
        '''required param security_group_id'''
        return {"ImageId": "ami-04763b3055de4860b", "KeyName": "keyZ", "MaxCount": 3, "MinCount": 3, "Monitoring":{"Enabled":False}, "SecurityGroupIds":[security_group_id]}

    def create_instances(self,params):
        '''create ec2 instances, must set security_group_id from 'getDefaultEC2Params'''
        result = self.ec2.create_instances(**params)


class Keys:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.LOCAL_DIRECTORY = '/Users/si3mshady/'
        self.TARGET_DIRECTORY = '/home/ubuntu/.ssh/'
        self.KEY_NAME = 'keyZ.pem'
        self.response = self.ec2.describe_instances()
        self.targets = self.evaluate_list()


    def evaluate_list(self):
        '''I noticed sometimes the indexs to retrieve the public dns name alternates out of the 1st and 2nd indices'''
        targets_a = [dns.get('PublicDnsName') for dns in self.response['Reservations'][0]['Instances']]
        targets_b = [dns.get('PublicDnsName') for dns in self.response['Reservations'][1]['Instances']]
        if "" not in targets_a:
            target = targets_a
        else:
            target = targets_b
        return target

    def uploadPrivateKeys(self):   

        '''use paramiko to upload private key to EC2 instances'''
        for i, _ in enumerate(self.targets):
            key = paramiko.RSAKey.from_private_key_file(self.LOCAL_DIRECTORY + self.KEY_NAME)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.targets[i], username="ubuntu", pkey=key)
            ftp_client=client.open_sftp()
            ftp_client.put(self.LOCAL_DIRECTORY + self.KEY_NAME,self.TARGET_DIRECTORY + self.KEY_NAME)
            ftp_client.close()

    def tightenPrivateKeyPermissions(self):
        for i, _ in enumerate(self.targets):
            cmd = "chmod 400 /home/ubuntu/.ssh/keyZ.pem"
            key = paramiko.RSAKey.from_private_key_file(self.LOCAL_DIRECTORY + self.KEY_NAME)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.targets[i], username="ubuntu", pkey=key)
            client.exec_command(cmd)

#EC2 | SecurityGroup | Paramiko Practice - Exercise
#Create class to generate cluster of ec2 instances using same private key
#Use paramiko to upload the private key to each EC2 instance in the cluster
#Elliott Arnold 10-18-19
