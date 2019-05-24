import boto3, json 

client = boto3.client('ec2')

def get_instance_ids():
    response = client.describe_instances()
    instance_id_list = [[insta['InstanceId'] for insta in response['Reservations'][i]['Instances']] for i in range(len(response['Reservations']))]
    instance_id_strings = [i[0] for i in instance_id_list]
    return instance_id_strings  

def start_instances(event,context):
    print(event)
    instance_ids = get_instance_ids()
    response = client.start_instances(
        InstanceIds=instance_ids,
        DryRun=False)
    return response 

def stop_instances(event,context):
    instance_ids = get_instance_ids()
    response = client.stop_instances(
    InstanceIds=instance_ids,
    Force=True)
    return response 

def test_function():
    response = get_instance_ids()    
    http_response = {
         "statusCode": 200,
        "body": json.dumps(response)
         }    
    return http_response

    
 #learning hands-on with Udemy - Start / Stop EC2 instances using AWS Lambda and Serverless Framework
 #Elliott Arnold 5-23-19
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances
#https://serverless.com/framework/docs/providers/aws/guide/quick-start/

    
