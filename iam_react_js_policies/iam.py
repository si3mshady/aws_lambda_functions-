import json,boto3,pprint 

iam = boto3.client('iam')

def get_json_iam(arn,version):
    p = iam.get_policy_version( PolicyArn=arn,VersionId=version)
    return p['PolicyVersion']['Document']

def format_json_string(string):
    return string.replace("\'", "\"")
    

def lambda_handler(event,context):
    print(event)
    try:
        arn = json.loads(event['body'])['arn']
        version =  json.loads(event['body'])['version']
        data = pprint.pformat(get_json_iam(arn,version))
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' },
            'body': format_json_string(str(data)),
                "isBase64Encoded": False
            
        }
        
    except Exception as e:
        print(e)
    
   
#AWS IAM ApiGateway Lambda Python React Compnents 
#Make request to ApiGateway return IAM policy document to browser
#Practice with Modals and Sidebars
#Elliott Arnold 7-19-20  
#Learning React JS - Need to learn CSS for real
