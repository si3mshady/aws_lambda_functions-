import boto3, logging, psycopg2, openpyxl
from configparser import ConfigParser
from io import BytesIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_cli = boto3.client('s3')

DB_CONFIG = '/tmp/config.ini'

def begin(event,context):
    logger.info(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    getDBConfig(bucket)
    insert_data = openExcel(bucket,key)
    insertRDS(insert_data)


def getDBConfig(bucket):
    responseObj = s3_cli.get_object(Bucket=bucket, Key=DB_CONFIG.rsplit('/')[-1])
    cfg = responseObj['Body'].read()
    with open(DB_CONFIG,'wb') as config:
        config.write(cfg)

def openExcel(bucket,key):
    responseObj = s3_cli.get_object(Bucket=bucket, Key=key)
    excelBinaryData = responseObj['Body'].read()
    '''use BytesIO to load binary data, instead of writing to disk'''
    wb = openpyxl.load_workbook(BytesIO(excelBinaryData))
    sheet = wb.sheetnames[0]
    active_sheet = wb[sheet]
    insert_list = [x[0] for x in active_sheet.values]
    formatted_list = create_tuple_list(insert_list)
    return formatted_list

def create_tuple_list(array):
    '''returns properly formatted list of tuples for working with SQL syntax'''
    formatted = [tuple([val]) for val in array]
    return formatted

def config(filename=DB_CONFIG, section='postgresql'):
    '''parse conf file '''
    parser = ConfigParser()
    '''read the config'''
    parser.read(filename)
    '''get the section wanted'''
    db = {}
    if parser.has_section(section):
        print('Reading db config')
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]   #key value structure from file
    else:
        raise Exception('Section {0} is not found in {1} file'.format(section,filename))
    return db

def insertRDS(data_list):
    # %s denotes string value
    sql = "Insert INTO artists(name) VALUES (%s)"
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.executemany(sql, create_tuple_list(data_list))
        connection.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


#AWS Lambda practice: Triggering Lambda functions
#Function is triggered by the upload of a spreadsheet file (.xlsx) to s3
#The data is parsed and then written to (POSTGRE) RDS table in AWS
#Elliott Arnold 7-15-19
#si3mshady

#https://pandas.pydata.org/pandas-docs/version/0.20/io.html
#https://github.com/jkehler/awslambda-psycopg2/issues/3
#https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
#https://stackoverflow.com/questions/28526935/pg-ctl-error-while-loading-shared-libraries-libpq-so-5?lq=1
#https://github.com/psycopg/psycopg2/issues/892