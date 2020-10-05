import boto3, json
from chalice import Chalice, CORSConfig

app = Chalice(app_name='remote-control')
cors_config = CORSConfig(allow_origin='*')

ec2 = boto3.client('ec2')
data = ec2.describe_instances()

def get_ec2_instances():    
    return [insta['Instances'][0]['InstanceId'] for insta in data['Reservations']]

def start_instances(instance_id):       
    response = ec2.start_instances( InstanceIds=[instance_id], DryRun=False)
    return response 

def stop_instances(instance_id):    
    response = ec2.stop_instances(
    InstanceIds=[instance_id],
    Force=True)
    return response 

@app.route('/{instance_id}', cors=True)
def toggle_instance_status(instance_id):
    instanceMapping = {insta['Instances'][0]['InstanceId']:insta['Instances'][0]['State']['Name'] \
         for insta in data['Reservations']}

    if instanceMapping[instance_id] == 'running':
        stop_instances(instance_id)
    else:
        print('need to start instance')
        start_instances(instance_id)



@app.route('/', cors=True)
def index():
    return  {
          'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' },
            'body': json.dumps(get_ec2_instances()),
                "isBase64Encoded": False
            
       }
    


#AWS Chalice ApiGateway Lambda Python JS Jquery CSS practice
#Create a small remote control to turn on/off ec2 instances - use bootstrap and css
#Elliott Arnold 
#10-4-20 Covid 19 

