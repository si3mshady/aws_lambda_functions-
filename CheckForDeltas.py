import boto3
import json
import hashlib

dynamo = boto3.resource('dynamodb', region_name='us-east-1')
dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
ec2 = boto3.client('ec2')
sns = boto3.client('sns')
arn = "arn:aws:sns:us-east-1:952151691101:Rule_Change_Detected"


def main(event,context):
    '''check if table has been populated, if not populate table'''
    result = dynamo_client.scan(TableName='ConfigMonitor')
    if result['Count'] == 0:
        loadDDB()
    else:
        delta = compare(result)
        if len(delta) != 0:
           print(str(delta))

def get_current_config():
    results = ec2.describe_security_groups()
    processed_dictionary = genHashedDictionary(results)
    return processed_dictionary

def loadDDB():
    processed_dictionary = get_current_config()
    for key,val in processed_dictionary.items():
        putItem(dynamo,key,val)

def compare(res):
    '''compare current security group hash with that previously listed in ddb table,
    if deviation is detected, publish to an sns topic'''
    modified = []
    current_confg = get_current_config()
    scanned_dictionary = {result['groupID']['S']: result['hashedPolicies']['S'] for result in res['Items']}
    for i in scanned_dictionary:
        if i in current_confg:
            if current_confg[i] != scanned_dictionary[i]:
                modified.append(i)
                res = sns.publish(
                    TopicArn='arn:aws:sns:us-east-1:952151691101:SecG_changes',
                    Message=f'Rule Change Detected for: {i}')
    return modified

def genHashValue(data_dictionary):
    '''convert dictionary to string and encode into bytes - required for hexdigest method '''
    bytes = json.dumps(data_dictionary, sort_keys=True).encode()
    hashed_string_from_bytes = hashlib.sha256(bytes).hexdigest()
    return hashed_string_from_bytes


def genHashedDictionary(data_dictionary):
    '''use dictionary comprehension '''
    hashed_dictionay = {element['GroupId']: genHashValue(element['IpPermissions']) for element in  data_dictionary['SecurityGroups']}
    return hashed_dictionay


def putItem(resource,group_id,hashed_policy,table='ConfigMonitor'):
    response = resource.Table(table).put_item(
        Item={
            'groupID':group_id,
            'hashedPolicies':hashed_policy
        }
    )
    return response


#AWS Lambda practice: Security groups and dynamoDb: Evalaute changes in security group rules using
#MD5 hash. Rules are compared against last recorded hash in dynamodDb, if hash changes: the script will publish to an sns topic
#Elliott Arnold 8-14-19
#si3mshady





