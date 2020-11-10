import json, boto3

TABLE_NAME = "customer-phone"

dynamoClient = boto3.client('dynamodb',region_name='us-east-1')
dynamoResource = boto3.resource('dynamodb', region_name='us-east-1')


def getPhoneNumber(phoneNum):
    dynamoResultSet = dynamoClient.scan(TableName=TABLE_NAME)
    if phoneNum in [num['phoneNumber']['S'] for num in dynamoResultSet["Items"]]:
         return True
         
def storePhoneNumber(phoneNumber):
    dynamoResource.Table(TABLE_NAME).put_item( Item={ "phoneNumber":phoneNumber } )


def lambda_handler(event, context):
    try:
        cust_phone =  event['Details']['ContactData']['CustomerEndpoint']['Address']
        if getPhoneNumber(cust_phone):
            return  {
                'Greeting': 'Welcome back!'
            }
        else:
            storePhoneNumber(cust_phone)
            return {
                'Greeting': 'You are calling for the first time. We have saved your phone \
                number for faster service next time.'
            }
    except:
        pass 
        
        
#AWS Connect (Call Center) Lambda DynamoDb Python3 exercise
#Use lambda to determine if customer has dialed into IVR after receiving customer input
#Elliott Arnold DFW DMS 11-9-2020

        
    
    
   
