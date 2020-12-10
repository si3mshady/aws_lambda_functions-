import boto3, time

ssm = boto3.client('ssm')

cmds = ['cd /home/ec2-user; ls']


def runSSMCommands(instanceId):
    cmd_id_list = []
    for cmd in cmds:
        result = ssm.send_command(InstanceIds=[instanceId],DocumentName='AWS-RunShellScript', Parameters={'commands': [cmd]})
        time.sleep(3)
        cmd_id_list.append((lambda x: x['Command']['CommandId'])(result))
    return cmd_id_list



def lambda_handler(event,context):
    print(event)
    instanceId = event['instanceId']
    cmd_id_list = runSSMCommands(instanceId)
    return {'commandIds':cmd_id_list,'instanceId':instanceId}
    

#AWS StepFunctions Lambda SSM S3 practice exericse
#Create 3 state stage machine that will capture listing of files in directory and push to s3 
#Elliott Arnold Team DMS  
# 12-10-20 Covid-19  Mothership AWS  Everythings not lost 
#ThreeStateMachina 
