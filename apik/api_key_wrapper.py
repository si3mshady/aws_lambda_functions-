from functools import wraps
import boto3

#think of the params being applied to "new_event" as those 
#you will supply to the actual calling function in this case 'arg1','arg2'
class KeyManagment:
    @classmethod
    def store_authentication_information(cls,fn):
        @wraps(fn)
        def new_event(arg1,arg2):         
            ddbR = boto3.resource('dynamodb',region_name='us-east-1')
            dest_table = ddbR.Table('testing_api_keys')         
            apigw = boto3.client('apigateway')           
            user, email = fn(arg1,arg2)
            result = apigw.create_api_key(name=email,enabled=True)           
            api_key = result['value']
            api_key_id = result['id']
            dest_table.put_item(Item={str('email'): str(email), \
                            str('user'): str(user), \
                                str('api_key') : str(api_key), \
                                    str('api_key_id') : str(api_key_id) })            
        return new_event

    @classmethod
    def add_api_key_usage_plan(cls,fn):
        @wraps(fn)
        def new_event(arg):         
            email = fn(arg)
            apigw = boto3.client('apigateway')         
            ddb = boto3.client('dynamodb',region_name='us-east-1')
            ddb_result = ddb.scan(TableName='testing_api_keys')            
            api_key_id = [key['api_key_id'] for key in ddb_result['Items'] \
                 if key['email']['S'] == email ][0]['S']
            response = apigw.create_usage_plan_key(usagePlanId='tkfpit',
             keyId=api_key_id, keyType='API_KEY')
        return new_event
  


@KeyManagment.store_authentication_information
def get_username_email(arg1,arg2):                
            return arg1,arg2

@KeyManagment.add_api_key_usage_plan
def update_usage_plan(arg):    
    return arg

#AWS API Gateway Dynamo DB Usage API Key practice
#Create simple decorators to work with API
#Decorators provide additional functionality to methods
#When used, decorators generate api keys,
#updates DynamoDb table and assign api key to usage plan for use with authentication
#Elliott Arnold 6-11-20 





