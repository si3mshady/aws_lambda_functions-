import boto3
import random

class ALB_2_APIGW:
    def __init__(self,event):
        self.ec2 = boto3.client('ec2')
        self.alb =  boto3.client('elbv2')   
        self.lamba = boto3.client('lambda')    
        self.event = event        

    def get_active_listener_ports(self) -> list:
        data = self.alb.describe_listeners(LoadBalancerArn=self.get_alb_arn())       
        return [int(port['Port']) for port in (lambda x: x['Listeners'])(data)]
        #an iifee returns an iterable for use with list comprehension   

    def get_alb_arn(self) -> str:             
        return [arn['LoadBalancerArn'] for arn in self.alb.describe_load_balancers() \
            ['LoadBalancers']  if 'Sandbox' in arn['LoadBalancerArn'].split('/')[2]][0]

    def get_alb_sg(self) -> str:
        return [sg['SecurityGroups'][0] for sg in self.alb.describe_load_balancers()\
            ['LoadBalancers']   if 'Sandbox' in sg['LoadBalancerArn'].split('/')[2]][0]

    def get_new_target_group(self) -> str:
        kwargs = {"Name": self.event['detail']['responseElements']['functionName'], \
            "TargetType":"lambda"}
        response =  self.alb.create_target_group(**kwargs)           
        return (lambda x: x['TargetGroups'][0]['TargetGroupArn'])(response)  #iifee    

    def get_random_port(self) -> int:
        active_listener_ports = self.get_active_listener_ports()
        avail_port = random.randint(0,65535)
        if avail_port not in active_listener_ports:
            return avail_port    

    def add_alb_invoke_permissions(self,target_group_arn,fn_arn):
         #most critical function of class, alb must have perms to invoke function in target group 
        response = self.lamba.add_permission(
            FunctionName=fn_arn,
            StatementId='dynamically_created_' + str(self.get_random_port()),
            Action='lambda:*',
            Principal='*',
            SourceArn=target_group_arn           
        )

    def update_alb_sg(self,port):
        kwargs ={ "IpPermissions":[
            {
                'FromPort': int(port),
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'For testing purposes'
                    },
                ],
                'ToPort': int(port)
            },
        ], "GroupId": self.get_alb_sg()
            }  
        self.ec2.authorize_security_group_ingress(**kwargs)  
   

    def create_listener(self,port,target_group_arn):
        response = self.alb.create_listener(LoadBalancerArn=self.get_alb_arn(),
        #creating forwarding rule is required when using lambdas in target group
        Protocol='HTTP', Port=port, \
            DefaultActions=[ {'Type': 'forward', \
                'TargetGroupArn': target_group_arn,           
            'ForwardConfig': {'TargetGroups': \
                [ {'TargetGroupArn': target_group_arn, 'Weight': 2 },],} },])

    def process_alb_event_listener(self):   
        random_port = self.get_random_port()
        fn_arn = (lambda x: x['detail']['responseElements']['functionArn'])(self.event) #iifee
        target_group_arn = self.get_new_target_group()  
        self.add_alb_invoke_permissions(target_group_arn,fn_arn)
        self.alb.register_targets(TargetGroupArn=target_group_arn, \
             Targets=[{'Id':fn_arn,'AvailabilityZone': 'all' } ])
        self.update_alb_sg(random_port)
        self.create_listener(random_port,target_group_arn)

def lambda_handler(event,context):
    try:
        if 'CreateFunction' in event['detail']['eventName']:                      
            init = ALB_2_APIGW(event)          
            init.process_alb_event_listener()            
    except KeyError:
        pass

#AWS Lambda Application Load Balancer Practice
#Use lambda to register new functions to application load balancer 
#creating target groups, update security groups, adding listeners 
#Elliott Arnold DMS 6-16-20 

#https://github.com/aws/aws-cdk/issues/4663
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.add_permission
#https://docs.aws.amazon.com/lambda/latest/dg/API_AddPermission.html
##https://stackoverflow.com/questions/54072326/how-to-programmatically-register-a-lambda-listener-rule-to-an-alb

 
