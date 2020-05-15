import json
import random
import boto3

class BroadcastMessages:
    def __init__(self,event):
        self.event = event  
        self.stage = event['requestContext']['stage']
        self.api_id = event['requestContext']['apiId']
        self.region = 'us-east-1'
        self.domain = f'{self.api_id}.execute-api.{self.region}.amazonaws.com'
        self.management_url = f'https://{self.domain}/{self.stage}'
                         
        self.ddb_client = boto3.client("dynamodb")
        self.management_api = boto3.client("apigatewaymanagementapi", endpoint_url = self.management_url)

    def scan_db_map_data(self) -> dict:
        result = self.ddb_client.scan(TableName="connections_websocket")
        user_id_mapping = {val['connectionId']['S']:val['Username']['S'] for val in result['Items']}
        return user_id_mapping

    def parse_user_message(self) -> tuple:
        conection_id = self.event['requestContext']['connectionId']
        msg = json.loads(self.event['body'])['data']
        return conection_id, msg

    def broadcast(self):
        users = self.scan_db_map_data()
        conection_id, msg = self.parse_user_message()
                
        for val in users.keys():
            try:
                self.management_api.post_to_connection(ConnectionId=val,\
                    Data=f"User {users[conection_id]} posted {msg}".encode())
            except Exception:
                pass                
                   

def lambda_handler(event, context):
    print(event)    
    wss = BroadcastMessages(event)
    wss.broadcast()

#Serverless chat app - basic 
#Lambda, DynamoDb , Api gateway