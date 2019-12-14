import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    print(event)
    modify = ModAttribute()
    modify.change_instance_type()

class ModAttribute:

    def __init__(self):
        self.ec2 = boto3.client('ec2', region_name='us-east-1')
        self.sqs = boto3.client('sqs')


    def get_instance_id_type_mapping(self):
        return {data['Instances'][0]['InstanceId']: data['Instances'][0]['InstanceType'] for data in
                self.ec2.describe_instances()['Reservations']}


    def get_instance_type(self,instance_id):
        return self.get_instance_id_type_mapping()[instance_id]


    def change_instance_type(self):
        instance_id = self.filter_instances()[0]
        if instance_id != None:
            instance_class = ['t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge']
            #get current instance type
            instance_type = self.get_instance_type(instance_id)
            try:
                index = instance_class.index(instance_type)

                if index + 1 < len(instance_class):
                    try:
                        self.mod_instance(instance_id, instance_class[index + 1])
                    except ClientError:
                        pass
            except ValueError:
                pass


    def get_messages(self):
        # get the instance_id from the sqs queue
        queue = "https://sqs.us-east-1.amazonaws.com/705166095368/MON_IDLE_CPU"
        response = self.sqs.receive_message(QueueUrl=queue, MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10 )
        return response


    def filter_instances(self):
        return list(set([instance['Body'] for instance in self.get_messages()['Messages']]))


    def mod_instance(self,instance_id, instance_type):
        self.ec2.modify_instance_attribute(InstanceId=instance_id, InstanceType={'Value': instance_type })


#AWS EC2 practice exercise - Modifying EC2 instance attributes with Lambda
#Lambda Polls the SQS queue for instances that have been flagged by script as using High CPU over X period of time
#Once found the instance class is modified for better performance
#Quick and Dirty
#Elliott Arnold  12-14-2019

