
class RequestAuthorizer:  

    def parse_req_obj(self,**kwargs):       
        _type = kwargs['type']
        methodArn = kwargs['methodArn']
        httpMethod = kwargs['httpMethod']
        headers = kwargs['headers']
        user_agent = headers['User-Agent']
        username = headers['HeaderAuth1']

        if username == "si3mshady" and user_agent == 'python-requests/2.22.0':
            params = {"Action":"execute-api:Invoke","Effect":"Allow",\
                "Resource":methodArn,"principalId":username}
            return self.access_granted(**params)
        else:
            params =  {"Action":"execute-api:Invoke","Effect":"Deny",\
                "Resource":methodArn,"principalId":username}
            return self.access_denied(**params)
    
    def make_policy(self,**kwargs):
        action = kwargs['Action']
        effect = kwargs['Effect']
        resource = kwargs['Resource']             
        principal_id = kwargs['principalId']      

        statement= {}
        statement['Action'] = action
        statement['Effect'] = effect
        statement['Resource'] = resource

        policy_doc = {}
        policy_doc['Version'] = "2012-10-17"
        policy_doc['Statement'] = [statement]        
        
        principal = {}
        principal['principalId'] = principal_id
        principal['policyDocument'] = policy_doc
        return principal        

    def access_granted(self,**params): 
        return self.make_policy(**params)

    def access_denied(**params):        
        return self.make_policy(**params)

def lambda_handler(event,context):    
    print(event)
    ra = RequestAuthorizer()
    return ra.parse_req_obj(**event)
    

#AWS APIGW Lambda Req Authorizer 
#APIGW + Lambda exercies 
#Elliott Arnold 5-27-20
