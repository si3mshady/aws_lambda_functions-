from PIL import Image
import boto3, cStringIO

client = boto3.client('s3')

def thumbnail(event,context):
    #print structure of event to log 
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    image = fetch_image(bucket,key)
    thumbnail_fileObject = pymParticles(image)
    thumbnail_key = generate_thumbnail_key(key)
    thumbnail_to_s3(bucket,thumbnail_key,thumbnail_fileObject)
    print('Thumbnail sucessfully added to s3 bucket: ' + bucket)
    return "GoT"
        
def pymParticles(image):
    size = 128, 128
    fileObj = cStringIO.StringIO()  #return a StringIO-like stream for reading or writing
    copied_image = image.copy()
    copied_image.thumbnail(size)
    copied_image.save(fileObj, 'PNG')
    fileObj.seek(0)
    return fileObj
     
def fetch_image(bucket,key):
    s3_response = client.get_object(Bucket=bucket, Key=key)
    image_binary_data = s3_response['Body'].read()
    #cStringIO.StringIO requires a string that is encoded as a bytes string we can impersonate string or bytes data like a file.
    fileObj = cStringIO.StringIO(image_binary_data)
    open_image_file_object = Image.open(fileObj)
    return open_image_file_object

def thumbnail_to_s3(bucket,key,image_file_object):
    response = client.put_object(
        ACL='public-read',
        Body=image_file_object,
        Bucket=bucket,
        ContentType='image/png',
        Key=key )
    
    
def generate_thumbnail_key(string):
    split_string = string.rsplit('.', 1)
    return split_string[0] + "antman_.thumbnail.PNG" 



#Thumbnail Generator - AWS_Lambda - 5-19-19   Elliott Arnold    got 
#Using buffer modules(StringIO, BytesIO, cStringIO) 
#These buffer modules help us to mimic our data like a normal file which we can further use for processing.
#cStringIO.StringIO requires a string that is encoded as a bytes string
#https://docs.python.org/2/library/stringio.html
#https://pillow.readthedocs.io/en/3.0.x/reference/Image.html
#https://pillow.readthedocs.io/en/3.0.x/reference/ImageOps.html
#https://webkul.com/blog/using-io-for-creating-file-object/
#https://stackoverflow.com/questions/45473501/getting-pil-pillow-4-2-1-to-upload-properly-to-aws-lambda-py3-6
# docker run -v `pwd`:/working -it --rm ubuntu
