import boto3
ec2 = boto3.client('ec2')
ec2Resource = boto3.resource('ec2')

sg_list = ["sg-067fd407a5350c96e","sg-016934c304771db40"]


def compare(list_a,list_b):
    #the use of 'set' allows for comparing the values and removing duplicates
    if len(list_a) > len(list_b):

        missing_sg = set(list_a) - set(list_b)
          
        return list(set(list_a + list(missing_sg)))        
          
    elif len(list_b) > len(list_a):

        missing_sg = set(list_b) - set(list_a)
          
        return list(set(list_b)) + list(missing_sg)  
    else:
        return (list(set(list_b)) - list(set(list_a)))

def check_attached_security_groups(instance_id,security_group_list):

    current_instance = ec2Resource.Instance(instance_id)
      
    attached_security_groups = [group['GroupId'] for group in current_instance.security_groups]  
    
    required_groups = compare(security_group_list,attached_security_groups)
      
    complete_sg = list(set(required_groups + attached_security_groups))
      
    if len(complete_sg) != 0:
        current_instance.modify_attribute(Groups=complete_sg)

def lambda_handler(event, context):
    try:
        ec2_event = event
        instance_id = ec2_event['resources'][0].split('/')[-1]
        check_attached_security_groups(instance_id,sg_list)
    except KeyError:
        print(event)

#AWS Lambda EC2 Security Groups Cloudwatch 
#Elliott Arnold 
#Add SG to Instance when launched in VPC => running state 
#If SG's are attached then no action is taken 
#quick and dirty
#AWS DMS DFW
#7/13/20 
