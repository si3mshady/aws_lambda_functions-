import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
BUCKET_NAME = 'alexa-detect-images-tf'

def lambda_handler(event,context):
    if event['request']['type'] == "LaunchRequest":
            count = getS3Count()
            message = f"You have {count} files in your S 3 bucket"
            return process_response(message)

    elif event['request']['type'] == "IntentRequest":
        return main(event)

'''get file names from s3'''
def getS3Keys():
    response = s3.list_objects(Bucket=BUCKET_NAME)
    keys = [filename.get('Key') for filename in response['Contents']]
    return keys

def getS3Count():
    return len(getS3Keys())

'''preform image regognition with AWS rekognition'''
def detect_label(photo, bucket=BUCKET_NAME):
    response = rekognition.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}}, MaxLabels=5)
    item = [img.get('Name') for img in response['Labels']][0]
    return item

def process_response(message):
    speech_response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": message
            },
            "shouldEndSession": False
        }
    }
    return speech_response

def main(event):
    intent = event['request']['intent']['name']
    slot = event['request']['intent']['slots']
    s3_items = getS3Keys()

    if intent == "detectImage":
        if slot['number']['value'] is "0":
            detected = detect_label(s3_items[0])
            detection_message = f"Image number 1 is {detected}"
            return process_response(detection_message)

        elif slot['number']['value'] is "1":
            detected = detect_label(s3_items[1])
            detection_message = f"Image number 2 is {detected}"
            return process_response(detection_message)

        elif slot['number']['value'] is "3":
            detected = detect_label(s3_items[2])
            detection_message = f"Image number 3 is {detected}"
            return process_response(detection_message)

#Alexa Custom Skill & AWS Rekognition  practice
#Lambda function becomes triggered from voice prompts made to Alexa - intents, utterances and slots
#Image detection/recognition is preformed.
#Recognized image is communicated back from Alexa device.
#Elliott Arnold 10-1-19

#https://stackoverflow.com/questions/27742537/list-comprehensions-extracting-values-from-a-dictionary-in-a-dictionary

