import boto3
#this lambda needs kratos role also 
#bucket _arn arn:aws:s3:::atop-logs-sandbox
class ATPS3: 
    
    def __init__(self,instance_id):
        self.instance_id = instance_id
        self.ssm = boto3.client('ssm')
    
    def atop_to_s3(self):
        cmd =  "for i in $(ls /var/log/atop); do aws s3 cp /var/log/atop/$i s3://atop-logs-sandbox/$(curl http://169.254.169.254/latest/meta-data/instance-id)$i; done"
        self.ssm.send_command(InstanceIds=[self.instance_id],DocumentName='AWS-RunShellScript', Parameters={'commands': [cmd]})
    
def lambda_handler(event,context):
    instance_id = event['Records'][0]['Sns']['Message']
    checker = ATPS3(instance_id)
    checker.atop_to_s3()