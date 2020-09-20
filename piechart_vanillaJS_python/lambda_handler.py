import boto3, json

ec2 = boto3.client('ec2')


def process_data_set():
    #explanation of sequence: len -> list -> list_comp -> map -> lambda at bottom  for future reference 
    mapping = assess_all_instances()['data']
    result_mapping = {}
    us_east_1_running = len([ el for el in list(map(lambda x: x if x['region'] == \
        'us-east-1' and x['state']['Name'] == 'running' else None, mapping)) if el != None])
    
    us_east_1_stopped = len([ el for el in list(map(lambda x: x if x['region'] == \
        'us-east-1' and x['state']['Name'] == 'stopped' else None, mapping)) if el != None])

    us_east_1_terminated = len([ el for el in list(map(lambda x: x if x['region'] == \
        'us-east-1' and x['state']['Name'] == 'terminated' else None, mapping)) if el != None])


    us_west_1_running = len([ el for el in list(map(lambda x: x if x['region'] == \
        'us-west-1' and x['state']['Name'] == 'running' else None, mapping)) if el != None])

    us_west_1_stopped = len([ el for el in list(map(lambda x: x if x['region'] == \
        'us-west-1' and x['state']['Name'] == 'stopped' else None, mapping)) if el != None])

    us_west_1_terminated = len([ el for el in list(map(lambda x: x if x['region'] == \
        'us-west-1' and x['state']['Name'] == 'terminated' else None, mapping)) if el != None])

    result_mapping['us-east-1'] = {'running': us_east_1_running, 'stopped':  us_east_1_stopped, 'terminated': us_east_1_terminated}
    result_mapping['us-west-1'] = {'running': us_west_1_running, 'stopped':  us_west_1_stopped, 'terminated': us_west_1_terminated}

    return {'data': result_mapping}
  


def getRegions():    
    return  [region['RegionName'] for region in ec2.describe_regions()['Regions']]


    
def assess_all_instances():
    main_array = []
    for region in getRegions():
        ec2 = boto3.client('ec2',region_name=region)
        instances = ec2.describe_instances()
        for i in instances["Reservations"]:
           main_array.append({"region": region,"state":i['Instances'][0]['State'], "instance_id":i['Instances'][0]['InstanceId']})


    return {"data":main_array}

def lambda_handler(event,context):
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' },
            'body': json.dumps(process_data_set()),
                "isBase64Encoded": False
            
        }


    

# AWS ApiGateaway Lambda Vanilla JS  Python3 
# Create custom API w/ AWS Lambda and update pie chart using ChartJS framework 
# Elliott Arnold  9-20-20  Amazonian DMS DFW 

 #''' You must first define the what the lambda will return value  ie lambda x: x if x==2 else False {or None} 
 # Current examle returns matching element from list  otherwise returns None value. Must use Map in conjunction with Lambda to interate over 
# each element in list. Use list list comprehension to filter out the None values and 
# get the length with len)  len -> list -> list_comp -> map -> lambda '''