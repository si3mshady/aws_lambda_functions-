import string, random
import pulumi
import pulumi_aws as aws
from pulumi_aws import lambda_
import pulumi_docker as docker

docker_image_config = {"resource_name":"jenkins-root-user", \
    "docker_image":"si3mshady/jenkins-iam-root:latest"}

ports  = [{"external":"8080", "internal": "8080"}]

def get_random_string(length):   
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
    

rule_packages = {
        "CVE": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-gEjTy7T7",
        "OSSecConfigBenchmarks": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-rExsr2X8",
        "NetworkReachability": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-PmNV0Tcd",
        "SecurityBestPractices": "arn:aws:inspector:us-east-1:316112463485:rulespackage/0-R01qwB5Q"
}

class LambdaConfig:
    def __init__(self, args=None, custom=None) -> None:
        self.args = args 
        self.custom = custom 

    def dispatch_multiple_functions(self):
        for key, value in  rule_packages.items():             

            try:   
                aws.lambda_.Function(
                    f"Inspector-Function-{get_random_string(5)}",
                    code=pulumi.AssetArchive({'.': pulumi.FileArchive('./app.zip')}),
                    timeout= 30, 
                     handler="app.handler",
                    runtime="python3.8",
                    environment={
                        "variables": {
                            key: value
                        }
                    } ,
                    role="arn:aws:iam::888:role/lambda-kratos-exec-role"


                )
            except Exception as e:
                print(e)
           

class DockerConfig:
    
    def __init__(self, ports:list=ports,config:dict=docker_image_config) -> None:
        self.config = config
        self.ports = ports 

    def deploy_container(self):
        self.docker_resource = self.provision_docker_image(**self.config)
        self.launch_container = self.launch_container(self.config.get('resource_name'),\
            self.docker_resource, self.ports
        )
    
    def provision_docker_image(self, resource_name: str, docker_image: str) -> docker.RemoteImage:
        return docker.RemoteImage(resource_name=resource_name, name=docker_image)

    def launch_container(self, resource_name, docker_image_resource, ports)-> None:
        docker.Container(resource_name, \
            image=docker_image_resource.latest, ports=ports)

   
dg = DockerConfig(ports,docker_image_config)
dg.deploy_container()


lg = LambdaConfig()
lg.dispatch_multiple_functions()
