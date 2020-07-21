import boto3, json 

class RemoveDanglingTrigger:
    def __init__(self,event):        
        self._lambda = boto3.client('lambda') 
        self.s3 = boto3.client('s3')
        self.event = event         

    def iter_allS3_identify_dangling_lambda_from_bucket(self,fn):
        #list all s3 buckets 
        bkts  = [b['Name'] for b in  s3.list_buckets()["Buckets"]]
        for b in bkts:
             #get all notifications on s3 bucket
            val = self.filter_s3_bucket_for_dangling_lambda(bucket=b,lambda_fn=fn)
            if val != None:
                return val     

    def identified_bucket_get_policies(self,bucket):
        return (self.s3.get_bucket_notification_configuration(Bucket=bucket), bucket)


    def filter_s3_bucket_for_dangling_lambda(self,bucket,lambda_fn):
        b = self.s3.get_bucket_notification_configuration(Bucket=bucket)
        b = b.get('LambdaFunctionConfigurations',None)
        try:
            configured_funcs = {fn['LambdaFunctionArn'].split(':')[-1]:fn['Events']  for fn in b}
            #the lambda and event to remove 
            if lambda_fn in configured_fn_dict.keys():
                try:       
                    print("Policies in bucket",bucket)     
                    #identify s3 bucket and function associated to s3 that was deleted        
                    return {"bucket":bucket,lambda_fn:configured_funcs[lambda_fn]}
                except Exception as e:
                    pass
        except Exception as e:
            pass    
    
    def update_bucket_invoke_policy(self,arn,events,bucket):
        bconfig = 	{'LambdaFunctionConfigurations': [{            
                'Id': arn,
                'LambdaFunctionArn': arn ,
                'Events': events }               ]
                }        
        self.s3.put_bucket_notification_configuration(Bucket=bucket,\
            NotificationConfiguration=bconfig)          
    
    def parse_lambda_func_configs(self,lc_list,func_name):
        #from the function configs in the bucket 
        #identify the function and event config that has been deleted     
        for i in lc_list:
            if func_name in i['LambdaFunctionArn']:
                remove_value = i['LambdaFunctionArn']
        
         #S3 buckets lambdaConfigs minus the function that was deleted
        updated_policy = [x for x in lc_list \
            if x['LambdaFunctionArn'] != remove_value]

        return updated_policy


    def fix_bucket_lambda_config(self):        
        if "DELETE" in self.event.get('detail',None)['eventName'].upper():
            function_name =  self.event['detail']['requestParameters']['functionName']            
            bucket_info_dangling_lambda_dict = \
            
            self.iter_allS3_identify_dangling_lambda_from_bucket(function_name)
            
            lambda_configs_on_bkt, bucket =  self.identified_bucket_get_policies\
                (bucket_info_dangling_lambda_dict['bucket'])       
            
            lambda_configs_on_bkt = lambda_configs_on_bkt['LambdaFunctionConfigurations']  
            
            clean_config = self.parse_lambda_func_configs(lambda_configs_on_bkt,function_name)
            
            good_arn =  clean_config[0]['LambdaFunctionArn']
            
            events =  clean_config[0]['Events']
            
            self.update_bucket_invoke_policy(good_arn,events,bucket)
            

def lambda_handler(event,context):
    try:
        rdt = RemoveDanglingTrigger(event)
        rdt.fix_bucket_lambda_config()    
    except Exception as e:
        print(e)

#AWS Lambda S3 Python Boto3 Troubleshooting
#Remove Lambda Configurations from S3 bucket when assocaited lambda function is deleted
#Elliott Arnold  DMS 7-21-2020   
