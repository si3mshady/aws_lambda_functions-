class CustomAuth:
    def __init__(self,event):
        self.event = event
        self.token = self.event['authorizationToken']
        self.action = ['execute-api:Invoke']
        
    def evaluate_authorization(self):
        #return 200 
        if self.token.title() == 'Allow':
            return CreatePolicyDoc.gen_policy_document(action=self.action,effect=self.token)
        #return 403
        elif self.token.title() == 'Deny':
             return CreatePolicyDoc.gen_policy_document(action=self.action,effect=self.token)
        #return 401
        else:
            return CreatePolicyDoc.gen_policy_document()

class CreatePolicyDoc:           
    @classmethod
    def gen_policy_document(cls,effect='',action='',resource="*") -> dict:
        #policy response body mandatory fields principalId and policyDocument
        policy = {
            "principalId": "yyyyyyyy", 
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                {
                    "Action":cls.get_action_values(action),
                    "Effect": effect.title(),
                    "Resource": resource
                }
                ]
            }}
        return policy

    @classmethod
    def get_action_values(cls,action):
        if type(action) == list:
            return action
        else:
            return action

def lambda_handler(event,context):
    '''
    request must be in the format
    {'type': 'TOKEN', 'authorizationToken': <'Allow'|'Deny'>, 
    'methodArn': 'arn of the target API Endpoint'}
    authorizer authenticates to invoke url 
    '''    
    print(event)    
    authorizer = CustomAuth(event)
    return authorizer.evaluate_authorization()

#AWS Apigateway Lambda Token Authorizer 
#Serverless Practice 
#Elliott Arnold 5-22-20 


#https://console.aws.amazon.com/apigateway/home?region=us-east-1#/apis/nakuwetywj/authorizers
#https://stackoverflow.com/questions/41486130/aws-api-gateway-execution-failed-due-to-configuration-error-invalid-json-in-re
