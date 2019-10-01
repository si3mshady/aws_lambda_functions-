import boto3
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')


def getS3Keys():
    response = s3.list_objects(Bucket='alexa-detect-images-tf')
    keys = [filename.get('Key') for filename in response['Contents']]
    return keys

def getS3Count():
    return len(getS3Keys())



def detect_label(photo, bucket='alexa-detect-images-tf'):
    response = rekognition.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}}, MaxLabels=5)
    item = [img.get('Name') for img in response['Labels']][0]
    return item



#You have 3 items
#Item # is  #
def main():
    detected = []
    count = getS3Count()
    s3_items = getS3Keys()
    for item in s3_items:
        detected.append(detect_label(item))
    print(detected)