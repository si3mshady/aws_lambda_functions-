#!/bin/bash
yum update -y;
#install java8
yum install java-1.8.0-openjdk-devel -y
yum install git -y
git clone https://github.com/srimukh9/cleanjobhistory /home/ubuntu/cleanjobhistory
cd /home/ubuntu/cleanjobhistory
bash /home/ubuntu/cleanjobhistory/mvnw