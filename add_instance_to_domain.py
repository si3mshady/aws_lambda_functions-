import boto3
import os

class AddInstanceSubdomain:
    def __init__(self):
        self.access_key = os.environ.get('aws_access_key_id')
        self.secret_key = os.environ.get('aws_secret_access_key')
        self.r53 = boto3.client('route53',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key)
        self.ec2 = boto3.client('ec2',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key)
        self.hosted_zone = self.get_hosted_zone()
        self.vpc_id = 'vpc-b10096cb'

    def fetchall_instances(self):
            return self.ec2.describe_instances(Filters=[{'Name': 'vpc-id', 'Values': [self.vpc_id, ]}, ])

    def get_hosted_zone(self, domain='shadypythonista.com'):
            # return hosted  zone id
            return [i['Id'] for i in self.r53.list_hosted_zones()['HostedZones'] \
                    if domain in i['Name']][0].split('/')[-1]

    def add_complete_tag(self,instance_id):
        #tag instances once added to domain
        response = self.ec2.create_tags(
            DryRun=False,
            Resources=[
                instance_id
            ],
            Tags=[
                {
                    'Key': 'added to domain',
                    'Value': f'{instance_id}.shadypythonista.com'
                },
            ]
        )


    def check_instance_added_to_domain(self):
        try:
            for i in self.fetchall_instances()['Reservations']:

                if len(i['Instances'][0]['Tags']) >=1:

                    if len(i['Instances'][0]['Tags']) == 1:
                        if  'add_to_domain' in i['Instances'][0]['Tags'][0]['Key']:
                            self.add_subdomain(i['Instances'][0]['InstanceId'],i['Instances'][0]['PublicIpAddress'])

                    if len(i['Instances'][0]['Tags']) == 2:
                        if i['Instances'][0]['Tags'][1]['Key'] == 'added to domain':
                            print('Already_added',i['Instances'][0]['InstanceId'],i['Instances'][0]['PublicIpAddress'])

        except KeyError:
            pass

    def add_subdomain(self,instance_id,public_ip):
        self.r53.change_resource_record_sets(
            HostedZoneId=self.hosted_zone,
            ChangeBatch={
                'Comment': f'Adding subdomain {instance_id}.shadypythonista.com',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': f'{instance_id}.shadypythonista.com',
                            'Type': 'A',
                    'TTL': 120,

                            'ResourceRecords': [
                        {
                            'Value': public_ip
                        }],



                        }
                    },
                ]
            }
        )

        self.add_complete_tag(instance_id)

def lambda_handler(event,context):
    checker = AddInstanceSubdomain()
    checker.check_instance_added_to_domain()


#AWS Lambda DNS Route53 practice exercise
#Use cloudwatch trigger to check for new instances to add to public domain
#Instances carrying appropriate tag will have an create 'A' record and subdomain created allowing ssh access using public DNS name
#Elliott Arnold
#3-14-2020
