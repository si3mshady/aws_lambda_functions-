import subprocess


def mountFS():
    result = subprocess.check_output("lsblk | awk '{print $1}'", shell=True).decode()

    result_list = result.split('\n')

    if '' in result_list:
        result_list.remove('')

    output = subprocess.check_output(f"sudo file -s /dev/{result_list[-1]}", shell=True).decode()

    if ": data" in output:
        subprocess.check_output(f"sudo mkfs -t xfs /dev/{result_list[-1]}", shell=True).decode()
        output = subprocess.check_output(f"sudo mkdir /{result_list[-1]}", shell=True).decode()
        subprocess.check_output(f"sudo mount /dev/{result_list[-1]}  /{result_list[-1]}", shell=True).decode()


mountFS()



#AWS CloudWatch EBS Lambda Practice
#Triggering Lambda with Cloudwatch event 'Attach Partition'
#Once EC2 instance has a volume attached, lambda is triggered and the volume is mounted to the FileSystem
#Elliott Arnold
#11-26-2019
