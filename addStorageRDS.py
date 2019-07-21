import logging
import boto3
import json
import os

'''configure log level'''
logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''access environment variables'''
db_instance = os.environ['DB']
arn = os.environ['TOPIC']

'''access resources'''
client = boto3.client('rds')
sns = boto3.client('sns')

def addStorage(event,context):
    message_body = event['Records'][0]['Sns']['Message']
    trigger = json.loads(message_body)['Trigger']
    logging.info(trigger)
    modifyDbResponse = client.modify_db_instance(DBInstanceIdentifier=db_instance,
                                         AllocatedStorage=50,
                                         ApplyImmediately=True)
    response = sns.publish(TopicArn=arn, Message=str(trigger))


#AWS Lambda practice exercise - Using Cloudwatch - SNS and Lambda to monitor low storage condition on RDS.
#Fuction allocates additional storage to database when triggered and publishes to a SNS topic
#Elliott Arnold  7-20-19



#