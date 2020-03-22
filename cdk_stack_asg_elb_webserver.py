from aws_cdk import (
    aws_ec2 as ec2_stacker,
    aws_elasticloadbalancing as elb_stacker,
    aws_autoscaling as ats_stacker,  
    core)

class MyFirstCdkStackStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #return userdata script
        def get_userdata():
            with open('userdata.sh') as userdata:
                script = userdata.read()            
            return script

        #get public subnet 
        def get_public_subnet():
            public_subnet = covid_free_vpc.select_subnets(subnet_type=ec2_stacker.SubnetType.PUBLIC)
            return public_subnet.subnets[0]

        def get_web_sg():
            return covid_free_sg       
        
        #Generate 4 EC2 Instances 
        def generate_instances(count=4):
            amazon_linux_2 = ec2_stacker.GenericLinuxImage({"us-east-1": "ami-0fc61db8544a617ed"})      

            ec2_objects = []
            for i in range(count):
                ec2_instnace = ec2_stacker.Instance(self,f"Instance number {i}",instance_type=ec2_stacker.InstanceType('t2.micro'),
                machine_image=amazon_linux_2,vpc=covid_free_vpc,security_group=get_web_sg(),
                user_data=ec2_stacker.UserData.custom(get_userdata()))                
                ec2_objects.append(ec2_instnace)                
            return ec2_objects

        #utilty script, fetches instance ids/ references in cloudformation
        def get_instance_reference_ids():
            data = generate_instances()
            for i in data:
                yield(i.instance_id)         

        #create vpc with public & private subnet
        covid_free_vpc = ec2_stacker.Vpc(self, 'CovidFreeVPC',enable_dns_support=True,
        enable_dns_hostnames=True,max_azs=3, 
        subnet_configuration=[
        ec2_stacker.SubnetConfiguration(subnet_type=ec2_stacker.SubnetType.PUBLIC, name='InternetFacingSubnetGroup', cidr_mask=24)])
        #ec2_stacker.SubnetConfiguration(subnet_type=ec2_stacker.SubnetType.PRIVATE, name='PrivateSubnetGroup',  cidr_mask=24 )
        #])
        
        #creating security group requires vpc param 
        covid_free_sg = ec2_stacker.SecurityGroup(self,'CovidFreeSG',allow_all_outbound=True,vpc=covid_free_vpc)
        covid_free_sg.add_ingress_rule(peer=ec2_stacker.Peer.any_ipv4(),connection=ec2_stacker.Port.tcp(80),description="allow http traffic")
        covid_free_sg.add_ingress_rule(ec2_stacker.Peer.any_ipv4(),ec2_stacker.Port.tcp(22),description="allow ssh traffic")

        #create launch config (userdata is also a valid param)
        covid_free_lc = ats_stacker.CfnLaunchConfiguration(self,'CovidFreeLC',instance_type='t2.micro',image_id='ami-0fc61db8544a617ed' )

        #set up autoscaling group - better to add userdata from asg, does not throw base64 error. Able to use strings 
        instance_type = ec2_stacker.InstanceType.of(ec2_stacker.InstanceClass.BURSTABLE2, ec2_stacker.InstanceSize.MICRO)
        amazon_linux_2 = ec2_stacker.GenericLinuxImage({"us-east-1": "ami-0fc61db8544a617ed"})  
        covid_free_asg = ats_stacker.AutoScalingGroup(self,'CovidFreeASG',
        vpc=covid_free_vpc,associate_public_ip_address=True, key_name="CoronaVirusKP",instance_type=instance_type, machine_image=amazon_linux_2, min_capacity=5, max_capacity=10
        )
        covid_free_asg.add_user_data(get_userdata())

        #Register targets to ELB is an Autoscaling group, must be a list/array ot targets
        elb = elb_stacker.LoadBalancer(self,'CovidFreeELB',cross_zone=True,  vpc=covid_free_vpc,health_check={"port": 80},internet_facing=True,
        subnet_selection=get_public_subnet(), targets=[covid_free_asg])
        elb.add_listener(external_port=80)
        
      
   

#AWS #Cloudformation Clould Develop Kit practice
#Create a stack that includes VPC, Public Subnet, IGW, Route Table, Routes, Security Groupps, Classic LB, Launch Configuraiton, AutoScaling Group, Register ASG to LB, Basic Website 
#Elliott Arnold 3-21-20
#CVQuarantine 
#Youtube University, AWS Documentation, ACloudGuru, RTFM  

#Create a VPC with public subnet, igw, routes, route table 
#Create an ELB to be used to register web server instances.
#Auto Scaling Group and Launch Configuration that launches EC2 instances and registers them to the ELB
#Security Group allowing HTTP traffic to load balancer from anywhere (not directly to the instances).
#Some kind of automation or scripting that achieves the following Install and configure webserver
      
#references 
#pip install aws_cdk.aws_ec2
#pip install aws_cdk.aws_elasticloadbalancing
#pip install aws_cdk.aws_autoscaling

#what are tokens -> https://docs.aws.amazon.com/cdk/latest/guide/tokens.html
#https://youtu.be/pUAgg0TzSHw
#https://youtu.be/HDpnVuj6gUY
#agnostic stack error -> https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#ec2 instance construct -> https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Instance.html
#ec2 instance_type -> https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/InstanceType.html 
#autoscaling ->  https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_autoscaling.README.html
#userdata -> https://github.com/aws-samples/aws-cdk-examples/blob/master/python/existing-vpc-new-ec2-ebs-userdata/cdk_vpc_ec2/cdk_vpc_ec2_stack.py
#https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2.README.html#vpc
#https://docs.aws.amazon.com/cdk/api/latest/docs/aws-ec2-readme.html
#https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html
#add security group ingress rules -> https://stackoverflow.com/questions/57922113/add-ingress-rule-to-security-groups-using-aws-cdk
#loadbalancer -> https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_elasticloadbalancing.README.html
#selecting subnets -> https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-ec2.Vpc.html
