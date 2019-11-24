import boto3
import time

class Toggle_NACL:

    def __init__(self, network_acl_id='acl-02f93c4db1c5b9c5a'):
        self.ec2 = boto3.resource('ec2')
        self.network_acl = self.ec2.NetworkAcl(network_acl_id)

    '''prohibit all inbound/outbound traffic to subnet'''

    def subnet_offline(self):
        self.master_deny_ingress_rule()
        self.master_deny_egress_rule()

    '''permit all inbound/outbound traffic to subnet'''

    def subnet_online(self):
        self.master_allow_ingress_rule()
        self.master_allow_egress_rule()

    def twenty_sec_toggle_test(self):
        print(f'Locking down subnet {self.network_acl.associations[0]["SubnetId"]}.')

        self.subnet_offline()

        print(f'Subnet {self.network_acl.associations[0]["SubnetId"]} is unreachable.')

        time.sleep(20)

        print(f'Opening connections for subnet {self.network_acl.associations[0]["SubnetId"]}.')

        self.subnet_online()
        print(f'Subnet {self.network_acl.associations[0]["SubnetId"]} is now reachable.')

    def master_allow_egress_rule(self):
        response = self.network_acl.replace_entry(
            CidrBlock='0.0.0.0/0',
            DryRun=False,
            Egress=True,
            Protocol='-1',
            RuleAction='allow',
            RuleNumber=1
        )
        return response

    def master_allow_ingress_rule(self):
        response = self.network_acl.replace_entry(
            CidrBlock='0.0.0.0/0',
            DryRun=False,
            Egress=False,
            Protocol='-1',
            RuleAction='allow',
            RuleNumber=1
        )
        return response

    def master_deny_egress_rule(self):
        response = self.network_acl.replace_entry(
            CidrBlock='0.0.0.0/0',
            DryRun=False,
            Egress=True,
            Protocol='-1',
            RuleAction='deny',
            RuleNumber=1
        )
        return response

    def master_deny_ingress_rule(self):
        response = self.network_acl.replace_entry(
            CidrBlock='0.0.0.0/0',
            DryRun=False,
            Egress=False,
            Protocol='-1',
            RuleAction='deny',
            RuleNumber=1
        )
        return response

# AWS VPC  practice - learning to control ingress/egress traffic using NACL
# Basic Rules for Denying / Allowing all traffic into subnet
# Elliott Arnold
# 11-23-19