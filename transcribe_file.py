import boto3, time, json, os

transcribe_svc = boto3.client('transcribe')
S3 = boto3.client('s3')
sns = boto3.client('sns')
phone = os.environ['PHONE']

def init(event,context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    audio_uri = f"https://s3.amazonaws.com/{bucket}/{key}"
    print(audio_uri)
    job_name = f"job_{key}"
    aws_transcribe(transcribe_svc,job_name,audio_uri)
    time.sleep(600)
    json_result_key = job_name + '.json'
    txt = fetchJsonData(S3,json_result_key)
    sns.publish(PhoneNumber=phone,Message=str(txt))


def fetchJsonData(service,key,bucket='lambda-transcribe-code'):
    s3_response = service.get_object(Bucket=bucket, Key=key)
    resultData = s3_response['Body'].read()
    '''str to dict'''
    jsonResult = json.loads(resultData.decode())
    text = jsonResult['results']['transcripts'][0]['transcript']
    return text

def aws_transcribe(boto_svc,job_name,src_s3,output_bucket='lambda-transcribe-code'):  #init boto3 transcribeService
    result = boto_svc.start_transcription_job(TranscriptionJobName=job_name,
    LanguageCode='en-US',
    MediaSampleRateHertz=44100,
    MediaFormat='wav',
    Media={'MediaFileUri':src_s3},
    OutputBucketName=output_bucket,
    Settings={'ChannelIdentification': True })

#AWS Lambda practice: transcribing audiofiles - Lambda functions triggering lambda functions
#Function retrieves transcibed data from audio file, stores data into S3 , sending an sns message upon completion
#Elliott Arnold 7-11-19