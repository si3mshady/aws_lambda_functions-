import boto3,random,os,time,re


class ES_Util:
    def __init__(self,event):
        self.event = event
        self.es = boto3.client('es')     

    def get_domain_ep(self):
        dn = self.event['detail']['responseElements']['domainStatus']['domainName']
        response = self.es.describe_elasticsearch_domain(DomainName=dn)
        return (lambda x: x['DomainStatus']['Endpoints']['vpc'])(response)

    def get_vpc_id(self):
        return self.event['detail']['responseElements']['domainStatus']['vPCOptions']['vPCId']    

    def get_subnet_id(self):
        subnet_id = self.event['detail']['responseElements']['domainStatus']['vPCOptions']['subnetIds']
        return (lambda x: x[0])(subnet_id)

    def get_vpc_sg(self):
        sg = self.event['detail']['responseElements']['domainStatus']['vPCOptions']['securityGroupIds']
        return (lambda x: x[0])(sg)

class Run_CMD:
    def __init__(self,domain_ep):
        self.instance_id = 'i-070972dd8eafb4cf1' 
        self.ssm = boto3.client('ssm')        
        self.domain_ep = domain_ep       

    def run_ssm_cmd_get_result(self) -> list:
        cmd = "dig " + self.domain_ep + " | grep 'IN A' |  awk '{print $5}'"
        kwargs = {"InstanceIds":[self.instance_id],\
            "DocumentName":"AWS-RunShellScript","Parameters":{'commands': [cmd]}}      
        result = self.ssm.send_command(**kwargs)
        time.sleep(8)            
        cmd_id = (lambda x: x['Command']['CommandId'])(result)
        kwargs = {"CommandId":cmd_id,"InstanceId":self.instance_id}      
        result = self.ssm.get_command_invocation(**kwargs)['StandardOutputContent']          
        return [ip for ip in  result.split('\n') if ip != '' ]

class GET_NLB:
    def __init__(self):
        self.lb  = boto3.client('elbv2')          
        self.nlb_name = ''    
        self.nlb_arn = ''
        self.target_group_arn = ''
        self.listener_arn = ''
    
    def make_nlb_arn(self,subnet):
        self.nlb_name = 'lnt-automation-lb-' + str(random.randint(0,65535))
        params = {"Name":self.nlb_name, "Subnets": [subnet],\
            "Scheme":"internal","Type":"network", "IpAddressType":'ipv4'}    
      
        self.nlb_arn =  (lambda x: x['LoadBalancers'][0]['LoadBalancerArn']) \
        (self.lb.create_load_balancer(**params))

    def make_ip_target_group(self,vpc_id,target_group_name):
        params = {"Name":"TG-" + target_group_name,"Protocol":'TCP',\
            "Port":80,"VpcId":vpc_id,"TargetType":'ip'}       
        self.target_group_arn = (lambda x:x['TargetGroups'][0]['TargetGroupArn']) \
        (self.lb.create_target_group(**params))
    
    def register_targets_to_target_grp(self,target_list):        
        try:
            targets =  list(map(lambda x:{'Id': x, 'Port': 80},target_list))
            params = {"TargetGroupArn": self.target_group_arn ,"Targets": targets}
            self.lb.register_targets(**params)         
        except Exception:
            pass 

    def create_listener(self):
        params = {"LoadBalancerArn":self.nlb_arn, \
            "Protocol":'TCP', "Port":80, "DefaultActions":[ {'Type': 'forward', \
                'TargetGroupArn': self.target_group_arn, 'ForwardConfig': {'TargetGroups': \
                [ {'TargetGroupArn': self.target_group_arn},],}}]}        
        self.listener_arn = (lambda x:x['Listeners'][0]['ListenerArn'])\
        (self.lb.create_listener(**params))

class VPC_Link:
    def __init__(self):
        self.apigw =  boto3.client('apigateway')
        self.target_nlb_arn = ''        

    def make_vpc_link(self,nlb_arn):
        params = {"name": "lnt-automated-vpc-link-"  + str(random.randint(0,65535)) , "targetArns":[nlb_arn]}
        self.target_nlb_arn  =  self.apigw.create_vpc_link(**params)['targetArns'][0]


def lambda_handler(event,context):
    try:
        if 'CreateElasticsearchDomain' == (lambda x: x['detail']['eventName'])(event):
            main(event)            
    except IndexError:
        pass

def main(event):
     es_util = ES_Util(event)
     run_cmd = Run_CMD(es_util.get_domain_ep())
     cluster_ips = run_cmd.run_ssm_cmd_get_result()
     get_nlb = GET_NLB()
     get_nlb.make_nlb_arn(es_util.get_subnet_id())
     get_nlb.make_ip_target_group(es_util.get_vpc_id(),get_nlb.nlb_name)
     get_nlb.register_targets_to_target_grp(cluster_ips)
     get_nlb.create_listener()
     time.sleep(360)
     vpc_link = VPC_Link()
     vpc_link.make_vpc_link(get_nlb.nlb_arn)


#AWS #ElasticSearch #SSM #VpcLink #troubleshooting #practice 
# Elliott Arnold  6-16-20
#lambda gets correct event from elasticSearch Cluster, vpc id -done
#run dig cmd on SSM controlled EC2 to get the cluster_ip's  -done 
#get ips and create a NLB with Target Group, configure listener
#set up (REST) VPCLink pointing to NLB
#set up REST API with VPC link integration 


