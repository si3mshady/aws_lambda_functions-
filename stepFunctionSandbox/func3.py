import boto3, time 

ssm = boto3.client('ssm')
bucketName = 'stepfunctionoutput'



def copyToS3(instanceId,fileList):
    for file in fileList:
        ssm.send_command(InstanceIds=[instanceId],DocumentName='AWS-RunShellScript', \
        Parameters={'commands': [f"aws s3 cp /home/ec2-user/{file} s3://{bucketName}/{file}"]})
        time.sleep(3)
   

def lambda_handler(event, context):
    print(event)
    instanceId = event['instanceId']
    resultList = event['resultList']    
    copyToS3(instanceId,resultList[:10])    #just copy the first 10 
    
  
    return {
        'statusCode': 200,
        'body': 'Success!'
    }



#AWS StepFunctions Lambda SSM S3 practice exericse
#Create 3 state stage machine that will capture listing of files in directory and push to s3 
#Elliott Arnold Team DMS  
# 12-10-20 Covid-19  Mothership AWS  Everythings not lost 
#ThreeStateMachina 
