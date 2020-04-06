from aws_cdk import (core, aws_ec2, aws_iam)

class WebhookProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        def get_userdata():
            with open('bootstrap.sh', 'r') as userdata:
                return userdata.read()

        vmie_ami = "ami-00bf35d2ab0bdb452"
        default_vpc = "vpc-e94d1f93"
        ec2_role = "arn:aws:iam::88888888888:role/KratosRole"
        account_id = "8888888888"
        vm_import_image = aws_ec2.GenericLinuxImage({"us-east-1": vmie_ami})
        core.Environment(account=account_id)
        kratos_role = aws_iam.Role.from_role_arn(self, 'KratosXL', role_arn=ec2_role)

        aws_ec2.Instance(self, f"VMIE-{vmie_ami}", instance_type=aws_ec2.InstanceType('t2.micro'),
        role=kratos_role, machine_image=vm_import_image,  security_group=aws_ec2.CfnSecurityGroup(self, id=f"SG-{vmie_ami}",
        group_description=f"SG-CDK-{vmie_ami}"), vpc=aws_ec2.Vpc.from_lookup(self, f'CDK-VPC--{vmie_ami}', vpc_id=default_vpc),
        user_data=aws_ec2.UserData.custom(get_userdata()),   key_name="covidQuarantine")

