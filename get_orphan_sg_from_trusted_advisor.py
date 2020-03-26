import boto3, xlrd, re, os

class GetOrphanSG:
    def __init__(self,filepath: str):
        self.ec2 = boto3.client('ec2')
        self.filepath = filepath if (os.path.isfile(filepath) == True) else exit()
        self.get_orphan_sg()

    def load_excel_file(self):
        try:
            workbook = xlrd.open_workbook(self.filepath)
            sheet = workbook.sheet_by_index(0)
            if "security groups" in sheet.cell(0, 0).value.lower():
                sg = list((val for val in sheet.col_values(2) if val != '' and 'sg' in val))
                parsed_sg = [re.sub(r"\(vpc-[\S]+",'',val) for val in sg]
                return set(parsed_sg)
        except FileNotFoundError:
            print('File ' + self.filepath + ' not found.')

    def check_sg_instance_association(self):
        return set([i['Instances'][0]['SecurityGroups'][0]['GroupId']for i in self.ec2.describe_instances()['Reservations']])

    def get_orphan_sg(self):
        with open('orphaned_sg.txt', 'w') as ink:
            trusted_advisor_flagged_sg = self.load_excel_file()
            instances_with_sg = self.check_sg_instance_association()
            ink.write(str(trusted_advisor_flagged_sg.difference(instances_with_sg)))

if __name__ == "__main__":
    while True:
        path = input("Please enter full path to spreadsheet>  ")
        if not path.endswith('.xls'):
            print("Please ensure spreadsheet extension ends with .xls")
            continue
        else:
            break
    checkSg = GetOrphanSG(path)

#AWS Trusted Advisor practice
#Parse list of vulnerable security groups determine which groups are not associated with EC2 instance
#Elliott Arnold 3-26-20


