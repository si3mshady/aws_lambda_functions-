import subprocess
import boto3
FFMPEG_STATIC_TMP = "/tmp/ffmpeg"

client = boto3.client('s3')

def init(event,context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    make_wavs(bucket,key)

def make_wavs(bucket,key):
    s3_response = client.get_object(Bucket=bucket, Key=key)
    s3_response_ffmpeg = client.get_object(Bucket='lambda-code-aws', Key='ffmpeg')
    audio_data = s3_response['Body'].read()
    ffmpegExe = s3_response_ffmpeg['Body'].read()
    pathToMp3 = '/tmp/' + key.split('.')[0] + '.mp3'
    pathToWav = '/tmp/' + key.split('.')[0] + '.wav'
    with open(pathToMp3, 'wb') as ad:
        ad.write(audio_data)
    '''Download ffmpeg binary from s3 bucket, save it in /tmp/ good technique'''
    with open(FFMPEG_STATIC_TMP, 'wb') as ffmpeg:
        ffmpeg.write(ffmpegExe)
    cmd = f"chmod 755 {FFMPEG_STATIC_TMP}"
    data = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    cmd2 = FFMPEG_STATIC_TMP + " -i " + pathToMp3 + " " + pathToWav
    data = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
    wavBinary = open(pathToWav,'rb')
    waveToS3(bucket,pathToWav,wavBinary)

def waveToS3(bucket,key,fileObj):
    response = client.put_object(
        ACL='public-read',
        Body=fileObj,
        Bucket=bucket,
        ContentType='audio/wav',
        Key=key.split('/')[-1] )

#AWS Lambda practice: convert MP3 audiofile to WAV file using lambda function
#function is triggered by the creation of a new mp3 file in s3 bucket
#Elliott Arnold 7-10-19
# si3mshady