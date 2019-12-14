#!/bin/python3
import subprocess
import boto3
import time

class PIM:
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    sqs = boto3.client('sqs',region_name='us-east-1')
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
    def get_instance_id(cls):
        #get instance id from metadata service

        curl_metadata_service = 'curl http://169.254.169.254/latest/meta-data/instance-id'
        return subprocess.check_output(curl_metadata_service,shell=True).decode('utf-8')

    @classmethod
    def update_sqs(cls,instance_id):
        queue = "https://sqs.us-east-1.amazonaws.com/705166095368/MON_IDLE_CPU"
        cls.sqs.send_message(QueueUrl=queue, MessageBody=str(instance_id))

    @classmethod
    def run_metric_for_minute(cls):
        count = 0
        for i in range(61):
            percent_idle = cls.put_idle_metric()
            if percent_idle < float(20):
                count +=1

            time.sleep(1)

        if count > 59:
            instance_id = cls.get_instance_id()
            cls.update_sqs(instance_id)


PIM.run_metric_for_minute()


#AWS EC2 SQS Cloudwatch practice exercise - Sending custom EC2 metrics to cloudwatch
#Script runs from cron job checking the 'Idle/CPU' Percentage Metric at regular intervals (isostat)
#The script updates Cloudwatch and Sends messages to SQS when thresholds are reached.
#Quick and Dirty
#Elliott Arnold  12-14-2019