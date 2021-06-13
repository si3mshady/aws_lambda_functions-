import re , boto3, json
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

app = App(process_before_response=True)
ssm = boto3.client('ssm', region_name='us-east-1')
sm = boto3.client('secretsmanager', region_name='us-east-1')
secrets = sm.get_secret_value(SecretId='login').get('SecretString')
secrets = json.loads(secrets)

def run_commands_ssm(fields):
    #use ssm to run command on managed instance which is running selenium container
    try: 
        cmd_args = " ".join(fields)
        #slack converts ampersand to '%40' which causes add user to fail in broswer
        cmd_args = cmd_args.replace('%40','@')  
        cmd = f'sudo docker run  si3mshady/headless-ec2-adduser:1 {cmd_args}'  
        print(cmd)  
        return ssm.send_command(InstanceIds=[secrets.get('instance_id')],DocumentName='AWS-RunShellScript',
            Parameters={'commands': [cmd]})
    except TypeError:
        pass

@app.command("/create_workspace")
def create_workspace_user(ack, say, body, respond, command):
    print('this is the body')
    #command arguments are transformed into a string with spaces         
    username = body.get('text').split(" ")[0]
    # Acknowledge command request    
    ack()
    say( f"Creating AWS workspace User => {username} 👍")
        

def process_create_command_data(data):
    
    pattern = r"create_workspace\S+text=([\w\+\.&%]+)&"
    try: 
        m = re.search(pattern, data)

        fields =  m.group(1).split('+')
        if len(fields) != 4:        

            return {
                "message":"Create command requires (4) attributes"
            }
        return fields
    except Exception as e:
        pass



def handler(event, context):
    print(event.get('body'))
    slack_handler = SlackRequestHandler(app=app)   
    fields  = process_create_command_data(event.get('body'))
    print(fields)
    result = run_commands_ssm(fields)
    print(result)    
    return slack_handler.handle(event, context)

#Elliott Arnold 
#Slackbot using slackbolt -> Lambda -> SSM -> Docker create AWS Workspace user  
#6-13-21
#wip 
