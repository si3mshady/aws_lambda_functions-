import boto3

class ServiceQuotas:
    def __init__(self,event):
        self.event = event 
        self.sq = boto3.client('service-quotas')
        self.sq_document = self.list_all_services_with_quotas()

    def list_all_services_with_quotas(self):
        sq_document = {}
        all_services = self.sq.list_services()
        for service in all_services.get('Services'):
            result = self.sq.list_service_quotas(ServiceCode=service['ServiceCode'])
            #some services have no list of quotas, so disreguard 
            if len(result['Quotas']) > 1:
                sq_document[service['ServiceCode']] = result                 
                
        return sq_document
    
    def get_service_quota_details(self,service_code):
        service_detail = self.sq_document[service_code]['Quotas']
        quota_names = [quotaName['QuotaName'] for quotaName in service_detail]
        return quota_names

    def get_service_names(self):
        return [sn for sn in self.sq_document]        

def lambda_handler(event,context):
    if event.get('httpMethod', None) == 'GET':
        sq = ServiceQuotas(event)
        data = sq.get_service_names()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' },
            'body': (str(data)),
                "isBase64Encoded": False
        }
        
    elif event.get('httpMethod', None) == 'POST':
        sq = ServiceQuotas(event)
        service_code = event.get('body').split('=')[-1]
        if service_code in sq.get_service_names():
            data = sq.get_service_quota_details(service_code)
            return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*' },
            'body': (str(data)),
                "isBase64Encoded": False
            
        }
            
        
#AWS Python Boto3 Lambda API-Gateway Practice
#Obtain service quota information via http request using Boto3, Lambda and APIGW
#Elliott Arnold DMS DFW 7-28-20  Part 1  -> TBC 
#Covid19

