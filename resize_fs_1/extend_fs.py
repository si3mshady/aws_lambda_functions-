import subprocess, re, time


def extend_partition():
    string_list = subprocess.check_output("lsblk | awk '{print $1}'", shell=True)
    # parse device name and partition
    # filter out empty lists and convert filter object to list
    matches = list(filter(None, [re.findall('([a-z0-9]{1,5})', element) for element in string_list.decode('utf-8').split('\n')]))

    extend_partition = [f'sudo growpart /dev/{matches[0][0]} 1', f'sudo  xfs_growfs  /dev/{matches[1][0]}']

    for cmd in extend_partition:
        subprocess.check_output(cmd, shell=True)
        time.sleep(8)


extend_partition()

#AWS Lambda Cloudwatch EBS Alarm Simulation
#Increase root ebs volume size and filesystem upon low storage condition
#Elliott Arnold
#12-5-19
