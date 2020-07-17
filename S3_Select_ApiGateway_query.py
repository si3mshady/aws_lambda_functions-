from collections import OrderedDict 
import boto3, json 
s3 = boto3.client('s3')

def lambda_validator(event):
    queryStringParams = event.get("queryStringParameters",None)
    if queryStringParams.get('query',None):
        return queryStringParams['query']

def make_ordered_dictionary(array):
    od = OrderedDict()
    for i in array:
        val = i.split(':')
        od[val[0]] = val[1]
    
    return od


def extract_from_s3(query,data):       
    body = data.get('body').split('&')    
    clean_result = [val.replace('=',':') for val in body]
    od = make_ordered_dictionary(clean_result) 

    bucket = od.get('Bucket')
    key = od.get('Key')
    
    params = {"Bucket": bucket, "Key": key,
    "ExpressionType":'SQL', "Expression": query,
     "InputSerialization": {'CSV': {"FileHeaderInfo": "Use"}},
    "OutputSerialization":{'CSV': {}}}
    
    result = s3.select_object_content(**params)

    #exract s3 payload, access csv data of file 
    
    v = [v for v in result['Payload']] #listcomprehension 
    
    document_data = v[0].get('Records')    
    return document_data
    

def lambda_handler(event,context):
    query = lambda_validator(event)
    if query:        
        data = extract_from_s3(query,event)
        resp = {'statusCode': 200,'headers': {'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' },'body': str(data),
                "isBase64Encoded": False  }

    return resp


#AWS Python3 APIgateway Lambda SQL S3Select 
#Make requests to ApiGateway; proxy requests to S3 Select and fetch data
#From CSV files in S3 
#Elliott Arnold - DMS DFW Covid19 Bee-Gees Night Fever 
