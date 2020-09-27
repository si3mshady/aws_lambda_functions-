#!/bin/bash

#update EC2 & prepare system to run flask on EC2 instance 
sudo yum update -y
sudo yum install -y gcc-c++ make
sudo yum install httpd -y
sudo chkconfig httpd on
sudo service httpd start
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo sed -i 's/AllowOverride None/AllowOverride ALL/g' /etc/httpd/conf/httpd.conf #critical
docker pull  si3mshady/miniwiki 
docker run --publish 888:888   si3mshady/miniwiki 
#needed to override default EC2 Apache settings  establish flask  
#AllowOverride directive is used to allow the use of .htaccess within the web server to allow
#overriding of the Apache config on a per directory basis.
#port forwarding syntax -> ssh -L [LOCAL_IP:]LOCAL_PORT:DESTINATION:DESTINATION_PORT [USER@]SSH_SERVER
#Docker Bash Userdata Port Forwarding Practice 
#Elliott Arnold 9-27-20
