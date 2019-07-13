import boto3
from hashlib import sha256
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_cli = boto3.client('s3')
ddb_res = boto3.resource('dynamodb', region_name='us-east-1')

def init(event,context):
    logger.info(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    hashedVal = hashfile(key,bucket,s3_cli)
    response = putItem(ddb_res,hashedVal,key)
    logger.info(response)

def hashfile(key,bucket,clientS3):
    response = clientS3.get_object(Bucket=bucket, Key=key)
    binary_data = response['Body'].read()
    hashed_value = sha256(binary_data).hexdigest()
    return hashed_value

def genDateString():
    now = datetime.now()
    dateString = now.strftime("%b-%d-%Y %H:%M:%S")
    return dateString

def putItem(resourceDDB,hashVal,filename,table='Metadata'):

    response = resourceDDB.Table(table).put_item(
        Item={
            'md5':hashVal,
            'filename':filename,
            'timestamp': genDateString()
        }
    )
    return response

#AWS Lambda Practice Exercises: S3 & DynamoDB - lambda function for hashing uploaded files and writing data to DDB
#Elliott Arnold 7-13-19
#si3mshady


