#!/bin/python3
import subprocess
import boto3
import time

class PIM:
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')    
    ssm = boto3.client('ssm')
    sns = boto3.client('sns')   
    
    percent_idle = "iostat | grep -A1 avg-cpu | column | awk '{print $6}' | grep '[0-9]'"

    @classmethod
    def put_idle_metric(cls):
        pi = float(subprocess.check_output(cls.percent_idle, shell=True).decode('utf-8'))
        cls.cloudwatch.put_metric_data(
                MetricData=[
                    {
                        'MetricName': 'Custom_Percent_Idle',
                        'Dimensions': [
                            {
                                'Name': 'Custom Data',
                                'Value': 'Percent_Idle'
                            },
                        ],
                        'Unit': 'Percent',
                        'Value': pi
                    },
                ],
                Namespace='Idle/CPU'
            )

        return pi

    @classmethod
    def publish_instance_id(cls):
        param = cls.ssm.get_parameter(Name='cdk-sns-arn')        
        sns_arn = param['Parameter']['Value']
        result = subprocess.Popen("curl http://169.254.169.254/latest/meta-data/instance-id",stdout=subprocess.PIPE,shell=True)
        instance_id = re.findall(r'(i-[0-9aA-zZ]+)',result.decode())[0]    
        cls.sns.publish(TargetArn=sns_arn, Message=instance_id)

    @classmethod
    def run_metric_for_minute(cls):
        count = 0
        for i in range(61):
            percent_idle = cls.put_idle_metric()
            if percent_idle > float(50):
                count +=1
            cls.publish_instance_id()
            time.sleep(1)


PIM.run_metric_for_minute()

#AWS EC2 SQS Cloudwatch practice exercise - Sending custom EC2 metrics to cloudwatch
#Script runs from cron job checking the 'Idle/CPU' Percentage Metric at regular intervals (isostat)
#Quick and Dirty
#Elliott Arnold  12-14-2019  -> (edited 3-28-20)
