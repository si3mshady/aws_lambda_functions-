from aws_cdk import (aws_lambda,aws_cloudwatch,aws_ec2,core,aws_iam,aws_events_targets,aws_sns,
aws_sns_subscriptions,aws_lambda_event_sources)


class DeployFirstLambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
     
        def get_userdata():
            with open('bootstrap.sh','r') as userdata:
                return userdata.read()     
              
        kratos_role = aws_iam.Role.from_role_arn(self,'KratosXL',
            role_arn="arn:aws:iam::88888888:role/KratosRole")
        
        lambda_role = aws_iam.Role.from_role_arn(self,'LambdaXL',
            role_arn="arn:aws:iam::999999999:role/Lambda_Kratos")

        sns_topic = aws_sns.Topic(self, "Topic", display_name="cdk-sns-trigger")            
    
        lambda_function  = aws_lambda.Function(self, "FetchAtopLogs",  runtime=aws_lambda.Runtime.PYTHON_3_6,role=lambda_role,
        handler="lambda_handler.lambda_handler", code=aws_lambda.Code.from_asset('myfunc'))

        lambda_function.add_event_source(aws_lambda_event_sources.SnsEventSource(sns_topic))
        sns_subscription = aws_sns_subscriptions.LambdaSubscription(lambda_function)

    
        def generate_instances(count=1):
            amazon_linux_2 = aws_ec2.GenericLinuxImage({"us-east-1": "ami-0fc61db8544a617ed"}) 
            ec2_objects = []
            for i in range(count):
                ec2_instnace = aws_ec2.Instance(self,f"CDK-Instance-{i + int(1)}",
                instance_type=aws_ec2.InstanceType('t2.micro'),
                role=kratos_role, machine_image=amazon_linux_2,
                security_group=aws_ec2.CfnSecurityGroup(self,id=f"SG{i + int(1)}",
                group_description=f"SG-CDK-{i}"),
                vpc=aws_ec2.Vpc.from_lookup(self,f'CDK-VPC-{i + int(1)}',
                vpc_id="vpc-eeeee3"),
                user_data=aws_ec2.UserData.custom(get_userdata()),
                key_name="covidQuarantine")                
                ec2_objects.append(ec2_instnace)                
            return ec2_objects
            
        generate_instances()
       

#AWS EC2 SQS SSM S3 Cloudwatch Cloudformation CDK  practice exercise -
#Bootstrap EC2 instances with ATOP and custom script to push instance metrics to Cloudwatch.
#Creates an SNS topic with a Lambda fuction subscription. The Lambda is trigged 
#bootsrapped python script publishes to the SNS topic when a metric threshold is breached. 
#Once breached the lambda uses Systems Manager (SSM) to execute a bash command to upload ATOP logs to S3
#Elliott Arnold 3-29-20    
#Covid19Quarantine 



#Resources 
#https://docs.aws.amazon.com/cdk/latest/guide/how_to_set_cw_alarm.html
#https://cdkworkshop.com/30-python/20-create-project/500-deploy.html
#https://linuxhint.com/bash-heredoc-tutorial/
#add admin permissions to ec2 instances for testing 
#https://aws.amazon.com/premiumsupport/knowledge-center/ec2-enable-epel/
#https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda_event_sources.html

