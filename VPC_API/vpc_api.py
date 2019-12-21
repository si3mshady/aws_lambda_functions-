from api_base import CustomRT,CustomSubnet,VPC_UTIL,MakeIGW,CustomVPC
from flask import Flask, jsonify, request
from flask_restful import Resource,Api

'''create app and wrap in in flask-restful'''
app=application=Flask(__name__)
api=Api(app)

class MakeVPC(Resource):
    def post(self):
        data = request.get_json()
        vpcCidrBlock = data.get('cidrBlock')
        if vpcCidrBlock != None:
            new_vpc = CustomVPC(vpcCidrBlock)
            return jsonify(vpc_id=new_vpc.vpc_id, message="VPC created successfully!")
        else:
            return jsonify(message="There was an ERROR creating the VPC.")

class MakeSubnet(Resource):
    def post(self):
        data = request.get_json()
        vpc_id = data.get('vpc_id')
        cidrBlock = data.get('cidrBlock')
        if vpc_id and cidrBlock !=None:
            new_subnet = CustomSubnet(vpc_id,cidrBlock)
            return jsonify(subnet_id=new_subnet.subnet_id, message="Subnet created successfully!")
        else:
            return jsonify(message="There was an ERROR creating the Subnet.")

class RouteTable(Resource):
    def post(self):
        data = request.get_json()
        vpc_id = data.get('vpc_id')
        if vpc_id != None:
            new_routeTable = CustomRT(vpc_id)
            return jsonify(route_table_id=new_routeTable.route_table_id, message="Route Table created successfully!")
        else:
            return jsonify(message="There was an ERROR creating the Route Table.")

class IGW(Resource):
    def post(self):
        new_igw = MakeIGW()
        return jsonify(igw_id=new_igw.igw_id, message="Internet Gateway created successfully!")

class AttachIGW(Resource):
    def post(self):
        data = request.get_json()
        igw_id = data.get('igw_id')
        vpc_id = data.get('vpc_id')
        if igw_id and vpc_id != None:
            response = VPC_UTIL.attach_igw(igw_id,vpc_id)
            if response == '200':
                return jsonify(message=f"IGW {igw_id} has attached to VPC {vpc_id} successfully!")
        else:
            return jsonify(message="There was an ERROR Attaching the IGW.")


class AssociateRT(Resource):
    def post(self):
        data = request.get_json()
        route_table_id = data.get('route_table_id')
        subnet_id = data.get('subnet_id')
        if route_table_id and subnet_id != None:
            response = VPC_UTIL.associate_rt(route_table_id,subnet_id)
            if response != None:
                return jsonify(association_id=response, message=f"Route Table {route_table_id} has successfully associated with Subnet {subnet_id}!")
            else:
                return jsonify(message="There was an ERROR Attaching Associating the Route Table with Subnet.")


class PublicRoute(Resource):
    def post(self):
        data = request.get_json()
        route_table_id = data.get('route_table_id')
        gateway_id = data.get('gateway_id')
        if route_table_id and gateway_id != None:
            response = VPC_UTIL.create_public_route(route_table_id,gateway_id)
            if response == True:
                return jsonify(message=f"Public Route has been configured for route {route_table_id}!")
            else:
                return jsonify(message="There was an ERROR creating the public route.")


api.add_resource(MakeVPC,'/makeVPC')
api.add_resource(MakeSubnet,'/makeSubnet')
api.add_resource(RouteTable,'/makeRT')
api.add_resource(IGW,'/makeIGW')
api.add_resource(AttachIGW,'/attachIGW')
api.add_resource(AssociateRT,'/associateRT')
api.add_resource(PublicRoute,'/makePublicRoute')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

#AWS VPC FLASK Practice
#Creating Custom VPCS, Subnets, Route Tables, IGW and Associations & Routes
#Use flask-restful to create a simple restful web api framework to configure VPC's
#Elliott Arnold 12-21-19



















