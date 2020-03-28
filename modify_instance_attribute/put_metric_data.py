#!/bin/python3
import subprocess
import boto3
import time

class PIM:
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')    
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
    def run_metric_for_minute(cls):
        count = 0
        for i in range(61):
            percent_idle = cls.put_idle_metric()
            if percent_idle < float(20):
                count +=1

            time.sleep(1)


PIM.run_metric_for_minute()

#AWS EC2 SQS Cloudwatch practice exercise - Sending custom EC2 metrics to cloudwatch
#Script runs from cron job checking the 'Idle/CPU' Percentage Metric at regular intervals (isostat)
#Quick and Dirty
#Elliott Arnold  12-14-2019  -> (edited 3-28-20)
