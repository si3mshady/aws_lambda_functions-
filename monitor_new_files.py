import subprocess, glob, time, paramiko
from pathlib import Path

class PollNewFiles:
    def __init__(self):
        self.files = self.poll_files()
        self.check_inventory_file_exists()

    def monitor(self):
        while True:
            time.sleep(5)
            self.files = self.poll_files()
            if len(self.check_new_files()) > 0:
                self.append_new_files()

    def poll_files(self):
        cmd = 'find . -maxdepth 1 -type f'
        return set(subprocess.check_output(cmd,shell=True).decode().split())


    def check_inventory_file_exists(self):
        if not glob.glob('*inventory*'):
            cmd = 'touch inventory.txt'
            subprocess.check_output(cmd, shell=True)

    def read_inventory(self):
        return set([file.strip() for file in open('inventory.txt').readlines()])


    def check_new_files(self):
        return self.files - self.read_inventory()


    def append_new_files(self):
             with open('inventory.txt','a') as ink:
                for new_file in self.check_new_files():
                    print(f'Adding {new_file} to inventory')
                    ink.write(new_file + '\n')
                    full_file_path = Path(new_file).resolve()
                    try:
                        SSH.sendfile(full_file_path)
                        time.sleep(5)
                        print(f'Adding {new_file} to EC2')
                    except OSError as e:
                        print(e)

class SSH:
    @classmethod
    def sendfile(cls,file):
        cls._target_directory = '/home/ubuntu/si3mshady/'
        cls.hostname = 'ec2-54-158-115-200.compute-1.amazonaws.com'
        cls.local_key = '/Users/si3mshady/keyZ.pem'
        cls.key = paramiko.RSAKey.from_private_key_file(cls.local_key)
        cls.client = paramiko.SSHClient()
        cls.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cls.client.connect(hostname=cls.hostname, username="ubuntu", pkey=cls.key)
        cls.ftp = cls.client.open_sftp()
        cls.ftp.put(str(file), cls._target_directory + str(file).split('/')[-1])
        cls.ftp.close()


if __name__ == "__main__":
    delta = PollNewFiles()
    delta.monitor()

#AWS #EC2 #Linux Practice - monitoring directory for new files - if new file detected the file is ssh'd to EC2 instance
#Elliott Arnold
#si3mshady
#11-4-19
