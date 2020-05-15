import json
import random
import boto3



class WebSocketConnect:
    #on websocket connect wscat -c  wss://888888.execute-api.us-east.amazonaws.com/test
    def __init__(self):        
        self.username = 'user_' + str(random.randint(0,99))
        self.ddb_table = self.get_ddb_table()

    def get_ddb_table(self):
        ddb = boto3.resource('dynamodb', region_name='us-east-1')
        return ddb.Table("connections_websocket")
    
    def update_db(self,connection_id):
        self.ddb_table.put_item(Item={"Username": self.username,"connectionId": connection_id})
        return 1


def lambda_handler(event, context):
    print(event)
    connection_id = event['requestContext']['connectionId']
    wss = WebSocketConnect()
    if connection_id:
        if wss.update_db(connection_id):
            return { "statusCode": 200, "body": 'Connected.' }
    