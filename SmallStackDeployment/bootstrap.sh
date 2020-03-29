#!/bin/bash

OUTPUT=~/put_metric_data.py
wget --output-document=$OUTPUT https://raw.githubusercontent.com/si3mshady/aws_lambda_functions-/master/modify_instance_attribute/put_metric_data.py

#make script executable 
chmod +x $OUTPUT

#update instance, install python3, atop boto3, set cron job to push metrics to cloudwatch 
yum update -y 
yum install epel-release -y
yum install python3 -y
yum  install python-pip -y
pip3 install boto3 
yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum-config-manager --enable epel
yum install atop -y

crontab<<EOF
*/5 * * * * $OUTPUT 
EOF
