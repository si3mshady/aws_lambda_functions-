import boto3
from botocore.exceptions import ClientError

class CustomVPC:
    def __init__(self,vpc_cidr='10.0.0.0/16'):
        if VPC_UTIL.check_valid_cb(vpc_cidr):
            self.ec2 = boto3.client('ec2')
            self.vpcCidrBlock = vpc_cidr
            self.vpc_metadata = self.makeCustomVPC()
            self.vpc_cb = self.vpc_metadata['CidrBlock']
            self.vpc_id = self.vpc_metadata['VpcId']

    def makeCustomVPC(self):
        return self.ec2.create_vpc(CidrBlock=self.vpcCidrBlock)['Vpc']

class CustomSubnet:
    def __init__(self,vpc_id,cidrBlk):
        self.ec2 = boto3.client('ec2')
        self.vpc_id = vpc_id
        self.cidrBlk = cidrBlk
        if VPC_UTIL.check_valid_cb(cidrBlk):
            self.subnet_metadata = self.make_subnet()
            if self.subnet_metadata != None:
                self.az_id = self.subnet_metadata['AvailabilityZoneId']
                self.az =  self.subnet_metadata['AvailabilityZone']
                self.subnet_id = self.subnet_metadata['SubnetId']

    def make_subnet(self):
        try:
            return self.ec2.create_subnet(CidrBlock=self.cidrBlk, VpcId=self.vpc_id)['Subnet']
        except ClientError as e:
            print(e)

class CustomRT:
    def __init__(self,vpc_id):
        self.ec2 = boto3.client('ec2')
        self.vpc_id = vpc_id
        self.rt_metadata = self.create_route_table()
        self.route_table_id = self.rt_metadata['RouteTableId']
        self.routes = self.rt_metadata['Routes']

    def create_route_table(self):
            return self.ec2.create_route_table(VpcId=self.vpc_id)['RouteTable']

class MakeIGW:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.igw_metadata = self.makeigw()
        self.igw_id =  self.igw_metadata['InternetGatewayId']

    def makeigw(self):
        return self.ec2.create_internet_gateway()['InternetGateway']


class VPC_UTIL:
    ec2 = boto3.client('ec2')

    @classmethod
    def associate_rt(cls,route_table_id,subnet_id):
        return cls.ec2.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)['AssociationId']

    @classmethod
    def check_valid_cb(cls, cidr):
        cidr = int(cidr.split('/')[-1])
        if cidr < 16 or cidr > 24:
            print('VPC Cidr block cannot be larger than /16 or smaller than /24')
            return False
        else:
            return True

    @classmethod
    def attach_igw(cls,igw_id,vpc_id):
        return cls.ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)['ResponseMetadata']

    @classmethod
    def create_public_route(cls,route_table_id,gateway_id):
        return cls.ec2.create_route(DestinationCidrBlock='0.0.0.0/0',RouteTableId=route_table_id,GatewayId=gateway_id)['Return']



#AWS VPC FLASK Practice
#Creating Custom VPCS, Subnets, Route Tables, IGW and Associations & Routes
#Use flask-restful to create a simple api to mak
#Elliott Arnold 12-21-19





