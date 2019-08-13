import boto3

ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')
sns = boto3.client('sns')
response = ec2_client.describe_security_groups(GroupIds=['sg-011b88e8dd44b13c3'])
check_egress = allowed_sg = ''

def eval_securityGroup(event, context):
    try:
        check_egress = response['SecurityGroups'][0]['IpPermissionsEgress'][0]['IpRanges'][0]['CidrIp']
    except:
        pass
    try:
        allowed_sg = response['SecurityGroups'][0]['IpPermissions'][0]['UserIdGroupPairs'][0]['GroupId']
    except:
        pass

def setEgress():
    response = ec2_client.authorize_security_group_egress(
        GroupId='sg-011b88e8dd44b13c3',
        IpPermissions=[
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '10.0.0.0/24',
                        'Description': 'For testing purposes'
                    },
                ],
                'ToPort': 5000
            },
        ])
    res = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:952151691101:SecG_changes',
        Message='Reset Egress Rule')

def setIngress():
    response = ec2_client.authorize_security_group_ingress(
        GroupId='sg-011b88e8dd44b13c3',
        SourceSecurityGroupName='DummyGroup')
    res = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:952151691101:SecG_changes',
        Message='Reset Ingress Rule')


if check_egress != '10.0.0.0/24':
    setEgress()

if allowed_sg != 'sg-07642620dd0e8cb28':
    setIngress()

#AWS Lambda practice - basic lambda function that tests for configuration changes in a security group
#if detected function resets the rule and message is published to an sns topic
#Elliott Arnold  8-12-19

