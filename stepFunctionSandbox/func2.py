import boto3, time

ssm = boto3.client('ssm')
#i-070972dd8eafb4cf1

def getSSMCommandResults(cmd_id,instanceId):
    resultList = []
    kwargs = {"CommandId":cmd_id,"InstanceId":instanceId}      
    result = ssm.get_command_invocation(**kwargs)['StandardOutputContent']        
    resultList = result.split('\n')  
    
    return resultList
    
def lambda_handler(event,context):
    print(event)
    instanceId = event['instanceId']
    if len(event) > 0:
        for cmd_id in event['commandIds']:
            resultList = getSSMCommandResults(cmd_id,instanceId)
            time.sleep(3)
    print(resultList)
    return {'instanceId':instanceId, 'resultList': resultList}

#AWS StepFunctions Lambda SSM S3 practice exericse
#Create 3 state stage machine that will capture listing of files in directory and push to s3 
#Elliott Arnold Team DMS  
# 12-10-20 Covid-19  Mothership AWS  Everythings not lost 
#ThreeStateMachina 

#AWS #Python3 #Stepfunctions #SystemsManager #Lambda  #S3 mashup practice exercise. As the world turns and time progresses I began to support another great aws service from the #DMS profile named Step functions. Step functions allow for orchestrating a series of AWS services or, in this case lambda functions, in a pre-determined order for accomplishing tasks, think #batchJobs. Step functions are defined using the Amazon State Language which are json documents with special keys required to dictate the flow of work within the state machine (first image).  For practice I decided to create a 3 stage state machine where the output of one lambda functions becomes the input of the next. Here i'm just capturing a listing of files under a given directory on an SSM managed instance and ultimately copy them to an S3 bucket. #practice #pythonic #scripting  #threeStateMachina #motherShipAWS