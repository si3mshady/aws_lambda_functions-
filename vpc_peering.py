import boto3

class AutoPeerVPC:
    def __init__(self,vpc1='',vpc2='',region='us-east-1'):
        self.ec2 = boto3.client('ec2')
        self.ec2r = boto3.resource('ec2')
        self.region = region
        self.vpc1 = vpc1
        self.vpc2 = vpc2
        self.vpc1_cidr = self.map_vpc_id_cidr()[self.vpc1]
        self.vpc2_cidr = self.map_vpc_id_cidr()[self.vpc2]
        self.available_igw = self.get_default_igw_id()
        self.add_igw_vpc()
        self.vpc1_subnet, self.vpc2_subnet = self.create_subnets()
        self.vpc1_rt, self.vpc2_rt = self.create_route_table()
        self.peering_id = self.create_peering_connection()
        self.accept_pc()
        self.add_peering_routes()
        self.add_igw_routes()
        self.associate_route_table_subnet()

    def map_vpc_id_cidr(self):
        return {vicr['VpcId']:vicr['CidrBlock'] for vicr in self.ec2.describe_vpcs(VpcIds=[self.vpc1,self.vpc2])['Vpcs']}

    def create_subnets(self):
        vpc_list = self.get_vpc_list()
        vpc_cidr_list = [self.vpc1_cidr,self.vpc2_cidr]
        new_subnets = []
        for index,vpc in enumerate(vpc_list):
            vpc = self.ec2r.Vpc(vpc_list[index])
            if int(vpc_cidr_list[index].split('/')[-1]) == 16:
                subnet = vpc.create_subnet(CidrBlock=vpc_cidr_list[index].split('/')[0] + '/20')
                new_subnets.append(subnet.id)
        return new_subnets[0],new_subnets[1]

    def get_vpc_list(self):
        return [self.vpc1, self.vpc2]

    def create_route_table(self):
        vpc_list = self.get_vpc_list()
        new_route_tables = []
        for index,vpc in enumerate(vpc_list):
            route = self.ec2r.create_route_table(VpcId=vpc_list[index])
            new_route_tables.append(route.id)
        return new_route_tables[0],new_route_tables[1]

    def create_peering_connection(self):
        pc = self.ec2.create_vpc_peering_connection(
            PeerVpcId=self.vpc2,
            VpcId=self.vpc1,
            PeerRegion=self.region
        )

        return pc['VpcPeeringConnection']['VpcPeeringConnectionId']

    def accept_pc(self):
        #accept peering connection
        self.ec2.accept_vpc_peering_connection(VpcPeeringConnectionId=self.peering_id)

    def map_vpc_igw(self):
        #map vpc id with igw
        return {vi['Attachments'][0]['VpcId']: vi['InternetGatewayId'] for vi \
                in self.ec2.describe_internet_gateways()['InternetGateways'] if len(vi['Attachments']) != 0}

    def get_default_igw_id(self):
        #get all gateways that are not attached with tag = 'peering'
        return [igw['InternetGatewayId'] for igw in self.ec2.describe_internet_gateways()['InternetGateways'] \
                if len(igw['Tags']) == 1 and igw['Tags'][0]['Key'].lower() == 'peering']

    def add_igw_vpc(self):
        #attach gateway to each vpc
        if len(self.available_igw) >= len(self.get_vpc_list()):
            for index,vpc in enumerate(self.get_vpc_list()):
                self.ec2.attach_internet_gateway(InternetGatewayId=list(self.available_igw)[index],VpcId=vpc)

    def add_peering_routes(self):
        #requester
        self.ec2.create_route(
            DestinationCidrBlock=self.vpc2_cidr,
            RouteTableId=self.vpc1_rt,
            VpcPeeringConnectionId=self.peering_id
        )
        #target
        self.ec2.create_route(
            DestinationCidrBlock=self.vpc1_cidr,
            RouteTableId=self.vpc2_rt,
            VpcPeeringConnectionId=self.peering_id
        )

    def add_igw_routes(self):
        try:
            self.ec2.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                RouteTableId=self.vpc1_rt,
                GatewayId=self.map_vpc_igw()[self.vpc1]
            )
        except KeyError:
            pass

        try:
                self.ec2.create_route(
                    DestinationCidrBlock='0.0.0.0/0',
                    RouteTableId=self.vpc2_rt,
                    GatewayId=self.map_vpc_igw()[self.vpc2]
                )
        except KeyError:
            pass


    def associate_route_table_subnet(self):
        self.ec2.associate_route_table(
            RouteTableId=self.vpc1_rt,
            SubnetId=self.vpc1_subnet,

        )

        self.ec2.associate_route_table(
            RouteTableId=self.vpc2_rt,
            SubnetId=self.vpc2_subnet,

        )
        
        
        
        
#Spring Forward 3-8-20
#Elliott Arnold
#AWS  VPC Peering Practice Script
#Provided two basic VPC's in same region,
#creates subnet, route table, routes, peering connections, subnet associations and peers both VPCs,


#2 igw w/ tag = peering
#vpc-1 '10.0.0.0/16' CIDR
#vpc-1 '192.168.0.0/16' CIDR





