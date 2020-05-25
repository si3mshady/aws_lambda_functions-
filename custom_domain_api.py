import boto3

#triggers when api is deployed
class CustomDomainAGW:
    def __init__(self,event):
        self.event = event
        self.r53 = boto3.client('route53',region_name='us-east-1')
        self.apigw = boto3.client('apigateway',region_name='us-east-1')
        self.acm = boto3.client('acm',region_name='us-east-1')             
        self.distribution_domain_name = ''
        self.new_sub_domain = ''
        self.distribution_hosted_zone_id = ''
    
    def begin(self):
        self.create_custom_domain_apigw()
        self.create_alias_record()
        self.map_custom_domain_api()    

    def get_hosted_zone(self domain='shady,pythonista.com'):
        return [zone['Id'] for zone in  self.r53.list_hosted_zones()['HostedZones'] if 'py' in zone['Name']][0].split('/')[-1]
            #output = ['/hostedzone/XXXXXXXXXX'] and is in list, so get first index and split on '/'      
    
    def get_acm_certificate(self):
        certs = self.acm.list_certificates()
        return [cert["CertificateArn"] for cert in certs['CertificateSummaryList'] if '*' in cert["DomainName"]][0]
            #*shady.pythonista.com       

    def create_custom_domain_apigw(self):
        _, apiId, _ , _ = self.construct_invoke_url()
        wildcard_domain_arn = self.get_acm_certificate()
        self.new_sub_domain = f"{apiId}.shadypythonista.com"
        res = self.apigw.create_domain_name(domainName=self.new_sub_domain, certificateArn=self.get_acm_certificate())
        self.distribution_domain_name = res['distributionDomainName']
        self.distribution_hosted_id = res['distributionHostedZoneId']

    def create_alias_record(self):
        _, apiId, _ , _ = self.construct_invoke_url()
        self.r53.change_resource_record_sets(
                    HostedZoneId=self.get_hosted_zone(),
                    ChangeBatch={
                        'Comment': f'Adding subdomain {apiId}.shadypythonista.com',
                        'Changes': [
                            {
                                'Action': 'CREATE',
                                'ResourceRecordSet': {
                                    'Name': str(f'{apiId}.shadypythonista.com'),
                                    'Type': 'A',
                                    'AliasTarget': {
                            'HostedZoneId': str(self.distribution_hosted_id),
                            'DNSName': str(self.distribution_domain_name),
                            'EvaluateTargetHealth': False
                        } 
                           }
                            },
                        ]
                    }
            )

    def construct_invoke_url(self) -> tuple:
        if self.event['detail']['eventName'] == 'CreateDeployment':
            api_id = self.event['detail']['requestParameters']['restApiId']
            if self.event['detail']['requestParameters']['createDeploymentInput']:
                stage = self.event['detail']['requestParameters']['createDeploymentInput']['stageName']            
                region = self.event['detail']['awsRegion']
                invoke_url =  f"https://{api_id}.execute-api.{region}.amazonaws.com/{stage}"                
                return (invoke_url,api_id,region,stage)                     
       
                   
    def map_custom_domain_api(self):
        _, apiId, _ , stage = self.construct_invoke_url()
        response = self.apigw.create_base_path_mapping(domainName=str(self.new_sub_domain),\
            restApiId=str(apiId),stage=str(stage))
               
      

def lambda_handler(event,context):
    print(event)
    monitor = CustomDomainAGW(event)
    monitor.begin()
   

#AWS Route53 APIGW Map Custom Domain to API endpoint 
#Apply user-friendly URL to REST api
#Elliott Arnold 5-25-20
        

              


           
            

       

