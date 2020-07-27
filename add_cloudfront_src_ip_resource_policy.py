import requests
import pprint
import json



def get_cf_ip_ranges(range_type='GLOBAL'):
    ip = 'http://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips'
    ranges  = requests.get(ip).json()
    if range_type.upper() == 'GLOBAL':
        return ranges['CLOUDFRONT_GLOBAL_IP_LIST']
    elif range_type.upper() == 'REGIONAL':
        return ranges['CLOUDFRONT_REGIONAL_EDGE_IP_LIST']


def allowListCFSourceIPs(resource,allowList):
    resource_policy =  {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": resource
            },
            {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": resource,
            "Condition": {
                "NotIpAddress": {
                "aws:SourceIp": allowList
                }
            }
            }
        ]
        }

    print(json.dumps(resource_policy))

    
    
    
if __name__ == "__main__":
    while True:
        ip_ranges = input("Type 'Regional' or 'Global' for Cloudfront IP Ranges> ")
        if ip_ranges.lower() == 'regional' or ip_ranges.lower() == 'global':
            break
        else:
            continue
    allowListCFSourceIPs(resource='execute-api:/*/*/*',allowList=get_cf_ip_ranges(ip_ranges))



    

