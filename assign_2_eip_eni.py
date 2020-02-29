import boto3

class Assign2EIP:
    def __init__(self, instance):
        self.instance_id = instance
        self.ec2 =  boto3.client('ec2')
        self.ec2R = boto3.resource('ec2')
        self.ssm = boto3.client('ssm')
        self.eni, self.attachment_id  = self.get_eni()
        self.assign_private_ip()
        self.eip_dict = self.generate_2_eip()
        self.private_ips = self.fetch_private_ips()
        self.associate_eip_private_ip()

    def get_eni(self):
        eni =  self.ec2R.Instance(self.instance_id)
        return (eni.network_interfaces_attribute[0]['NetworkInterfaceId'],eni.network_interfaces_attribute[0]['Attachment']['AttachmentId'])


    def assign_private_ip(self):
        result = self.ec2.assign_private_ip_addresses(NetworkInterfaceId=self.eni, SecondaryPrivateIpAddressCount=1)
        return result['AssignedPrivateIpAddresses'][0]['PrivateIpAddress']

    def generate_2_eip(self):
        data = self.ec2.describe_addresses()
        counter = []
        eip_dictionary = {}
        if len(data['Addresses']) == 0:

            for execute in range(2):
                data = self.ec2.allocate_address(Domain='vpc')
                public_ip = data['PublicIp']
                allocation_id = data['AllocationId']
                eip_dictionary[public_ip] = allocation_id
            return eip_dictionary

        if len(data['Addresses']) < 2:
            for i in data['Addresses']:
                if 'InstanceId' not in i.keys():
                    counter.append(i)
                if len(counter) < 2:
                    for execute in range(1):
                        data = self.ec2.allocate_address(Domain='vpc')
                        public_ip = data['PublicIp']
                        allocation_id = data['AllocationId']
                        eip_dictionary[public_ip] = allocation_id
                    return eip_dictionary

        else:
            data = self.ec2.describe_addresses()['Addresses']
            return {eip['PublicIp']:eip['AllocationId'] for eip in data}

    def associate_eip_private_ip(self):
        allocation_ids = [ai for ai in self.eip_dict.values()]
        for index, pip in enumerate(self.private_ips):
            print(allocation_ids[index], pip)
            self.ec2.associate_address(
                    AllocationId=allocation_ids[index],
                    InstanceId=self.instance_id,
                    PrivateIpAddress=pip)


    def fetch_private_ips(self):
        data = self.ec2.describe_network_interfaces(NetworkInterfaceIds=[self.eni])
        return [pip['PrivateIpAddress'] for pip in data['NetworkInterfaces'][0]['PrivateIpAddresses']]


def lambda_handler(event,context):
    instance_id = event['detail']['instance-id']
    go = Assign2EIP(instance_id)


#AWS Lambda EC2 Boto3 Practice
#Assign 2 Elastic IPs to same Elastic Interface quick & dirty lambda
#Elliott Arnold  2-29-20




