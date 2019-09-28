import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event,context):
    if event['request']['type'] == "LaunchRequest":
        return process_response("Would you like to start stop or count your instances")

    elif event['request']['type'] == "IntentRequest":
        return process_intent(event)

def process_intent(event):
    intent = event['request']['intent']['name']
    count = runningInstances()

    if intent == 'activateInstances':
        if count is not None:
            message = f"launching {count} instances"
            launchInstances()
        return process_response(message)

    elif intent == 'deactivateInstances':

        if count is not None:
            message = f"shutting down {count} instances"
            stopInstances()
        return process_response(message)

    elif intent == 'countInstances':

        if count is not None:
            message = f" you have {count} instances running"
        return process_response(message)


def process_response(message):
    speech_response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": message
            },
            "shouldEndSession": True
        }
    }
    return speech_response


def launchInstances():
    instance_ids = get_instance_ids()
    response = ec2.start_instances(InstanceIds=instance_ids,DryRun=False)
    return response

def stopInstances():
    instance_ids = get_instance_ids()
    response = ec2.stop_instances(InstanceIds=instance_ids,Force=True)
    return response


def runningInstances():
    running_instances = len(get_instance_ids())
    return running_instances


def get_instance_ids():
    response = ec2.describe_instances()
    instance_id_list = [[ec2['InstanceId'] for ec2 in response['Reservations'][i]['Instances']] for i in range(len(response['Reservations']))]
    instance_id_strings = [i[0] for i in instance_id_list]
    return instance_id_strings



#AlexaSkillsPractice - Amazon Echo - Created a basic Alexa skill with intents and utterances to start stop and count EC2 instances
#Elliott Arnold 9-17-19