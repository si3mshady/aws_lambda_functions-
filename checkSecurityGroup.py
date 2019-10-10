import boto3
from botocore.exceptions import ClientError

class CheckSecurityGroups:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.data = self.ec2.describe_security_groups()

    def ingressQuadZeroGroups(self):
        '''produces a generator containing all sec groups where ingress rule permits all traffic 0.0.0.0/0 '''
        for i, _ in enumerate(self.data['SecurityGroups']):
            try:
                if self.data['SecurityGroups'][i]['IpPermissions'][0]['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                    yield (self.data['SecurityGroups'][i]['GroupId'])
            except IndexError:
                pass

    def get_active_sg(self):
        '''retrieve security group of all ec2 instances'''
        self.ec2_resource = boto3.resource('ec2')
        response = self.ec2.describe_instances()
        instance_id_list = [[insta['InstanceId'] for insta in response['Reservations'][i]['Instances']] for i in
                            range(len(response['Reservations']))]
        for i in instance_id_list:
            self.instance = self.ec2_resource.Instance(i[0])
            sg = self.instance.security_groups
            active_groups = sg[0]['GroupId']
            yield (active_groups)

    def removeUnattachedSG(self):
        '''Determine which security groups
        allow all inbound traffic to an ec2 instance but does not have
        a dependent object (instance) associated'''
        check = CheckSecurityGroups()
        quadZero = list(check.ingressQuadZeroGroups())
        active = list(check.get_active_sg())
        while len(active) < len(quadZero):
            for i in quadZero:
                if i not in active:
                    try:
                        quadZero.remove(i)
                        response = self.ec2.delete_security_group(GroupId=i)
                    except ClientError:
                        pass

#AWS Security Group practice - Determine which security groups
#allow all inbound traffic to an instance which does not have a dependent object (instance) attached
#Elliott Arnold 10-9-19





