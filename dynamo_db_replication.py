import boto3

class ReplicateDDb:
    def __init__(self,event):
        self.event = event
        self.ddbR = boto3.resource('dynamodb',region_name='us-east-2')
        self.src_table,self.dest_table = self.get_source_dest_tables()
        
    def get_source_dest_tables(self) -> tuple:
        source_arn = self.event['Records'][0]['eventSourceARN']
        source_table = source_arn.split('/')[-3]
        destination_table = source_arn.split('/')[-3].replace('1','2')
        return (source_table,destination_table)        
        
    def process_event(self):       
        try:
            if self.event['Records']:                
                if self.event['Records'][0]['eventName'] == 'INSERT':
                    self.replicate_new_event_insert() 
                elif self.event['Records'][0]['eventName'] == 'MODIFY':
                    self.replicate_new_event_modify()
        except Exception as e:
            print(e)
            exit()

    def replicate_new_event_insert(self):             
        new_data_dictionary = self.event['Records'][0]['dynamodb']['NewImage']
        #record of insertion data into dynamodb table 
        kvp_list = list(new_data_dictionary.items())        
        key1 = kvp_list[0][0]
        data1 = [data for data in kvp_list[0][1].values()][0]
        
        key2 = kvp_list[1][0]
        data2 = [data for data in kvp_list[1][1].values()][0]
        
        dest_table = self.ddbR.Table(self.dest_table) 
        dest_table.put_item(Item={str(key1): str(data1),str(key2): str(data2)})
        
        return 1
    
    def replicate_new_event_modify(self):
        
        new_data_dictionary = self.event['Records'][0]['dynamodb']['NewImage']
        #creates a tuple of dictionaries - easier to work with 
        kvp_list = list(new_data_dictionary.items())
        #nested dictionaries 
        primary_key = kvp_list[0][0]        
        primary_key_value = [data for data in kvp_list[0][1].values()][0]
        update_column = kvp_list[1][0]        
        new_value = [data for data in kvp_list[1][1].values()][0]       

        dest_table = self.ddbR.Table(self.dest_table) 
        dest_table.update_item(Key={f'{primary_key}': f'{primary_key_value}'},\
        UpdateExpression=f"set {update_column} = :placeholder", \
             ExpressionAttributeValues={":placeholder":f"{new_value}" })
             
        return 1


    
def lambda_handler(event,context):
    print(event)
    replicator = ReplicateDDb(event)
    replicator.process_event()
    

#AWS #Lambda #DynamoDb Cross Region DDB Replication Practice 
#Use lambda to replicate ddb changes across regions - inserting new documents, modifiying existing documents  
#Primary key => string for simplicity 
#Elliott Arnold
#5-19-2020


