import boto3
import json
import time
from faker import Faker

class ProduceDummyData:
    def __init__(self,iterations):
        self.stream = boto3.client('kinesis')
        self.fake = Faker()
        self.interations = iterations        
        
    def fake_it_till_you_make_it(self):
        for _ in range(self.interations):
            shell = {}
            shell["Name"] = self.fake.name(),
            shell["Phone Number"] = self.fake.phone_number(),
            shell["SSN"] = self.fake.ssn()
            yield shell    
      

    def dont_cross_the_streams(self):
        for fake_data in list(self.fake_it_till_you_make_it()):
            self.stream.put_record(StreamName="dont_cross_the_streams", Data=json.dumps(fake_data),PartitionKey="888")
            time.sleep(1)
    
if __name__ == "__main__":
    producer = ProduceDummyData(8)
    producer.dont_cross_the_streams()
 

#AWS Kinesis Lambda Aurora practice 
#Elliott Arnold BLM
#6-5-20
