import boto3
import base64
import json
import os 

class Serverless_RDS_Connect:
    def __init__(self,event):       
        '''connect to aurora data api for querying rds db'''
        self.rds_data_client = boto3.client('rds-data')          
        self.db_secret_arn = self.db_credentials_secrets_store_arn()                
        self.cluster_arn, self.database_name = self.get_environment_variables()
        self.event = event

    '''kinesis event is encoded as base64 string '''
    def decode_base64_event(self) -> dict:
        decoded = base64.b64decode(self.event['Records'][0]['kinesis']['data']).decode()
        return json.loads(decoded)    

    def get_environment_variables(self) -> tuple:
         cluster_arn = os.getenv('cluster_arn')
         database_name = os.getenv('database_name')         
         return cluster_arn,database_name

    def get_sql_params(self) -> list:
        insert_values = self.decode_base64_event()

        sql_parameters = [ {'name':'name', 'value':{'stringValue': str(insert_values['Name'][0])}},
            {'name':'phone_number', 'value':{'stringValue': str(insert_values["Phone Number"][0])}},
            {'name':'ssn', 'value':{'stringValue': str(insert_values["SSN"])}}]
        return sql_parameters

    def get_insert_statement(self) -> str:
        sql = 'insert into Users (name, phone_number, ssn ) values (:name,:phone_number,:ssn)'
        return sql

    def db_credentials_secrets_store_arn(self) -> str:
        '''secrets manager holds db username and pw '''
        secret_client = boto3.client(service_name='secretsmanager')
        return secret_client.get_secret_value(SecretId='serverless')['ARN']

    
    def execute_sql_query(self):
        self.rds_data_client.execute_statement(secretArn=self.db_secret_arn,
        database=self.database_name,resourceArn=self.cluster_arn,
        sql=self.get_insert_statement(),parameters=self.get_sql_params())

def lambda_handler(event,context):
        try:
            if 'kinesis' in event['Records'][0]:
                serverless = Serverless_RDS_Connect(event)
                serverless.execute_sql_query()               
        except IndexError:
            pass

#AWS Kinesis Lambda Aurora practice 
#Elliott Arnold BLM
#6-5-20

