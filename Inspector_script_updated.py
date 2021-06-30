import boto3, time, os, random, string


try:

   rule_package_value  =  os.environ.get('CVE')
   rule_package_key = "CVE"
   
except Exception:
    pass 

try:
   rule_package_value =  os.environ.get('OSSecConfigBenchmarks')
   rule_package_key = "OSSecConfigBenchmarks"
except Exception:
    pass 

try:
   rule_package_value =  os.environ.get('NetworkReachability')
   rule_package_key = "NetworkReachability"
except Exception:
    pass 

try:
   rule_package_value =  os.environ.get('SecurityBestPractices')
   rule_package_key = "SecurityBestPractices"
except Exception:
    pass 




def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
    

class InspectorGadget():
   
    def __init__(self, targetAssessmentName, rules):
        self.inspector = boto3.client('inspector')
        self.rule_arns = list(map(lambda x: x, rules.values()))
        self.targetAssessmentName = targetAssessmentName
        self.randomString =  get_random_string(4)

    def checkForVulns(self):
        '''start sequence to check for vuls on EC2 instances'''
        resource_group_arn = self.create_resource_group()
        assessment_target_arn = self.create_assessment_target(resource_group_arn)
        assessment_template_arn = self.create_assessment_template(assessment_target_arn)
        assessment_run_arn = self.start_assesment_run(assessment_template_arn)
        time.sleep(600)
        self.stop_assessment_run(assessment_run_arn)
        result = self.get_assessment_report(assessment_run_arn)

        if result['status'] == 'FAILED':
            return 'ASSESSMENT FAILED'
        while result['status'] != 'COMPLETED':
            time.sleep(10)
            result = self.get_assessment_report(assessment_run_arn)
        return result['url']

    def create_resource_group(self):
        '''params 'key', 'value' '''
        resp = self.inspector.create_resource_group(
            resourceGroupTags=[
                {
                    'key': 'si3m',
                    'value': 'shady'
                },
            ]
        )

        return resp['resourceGroupArn']

    def create_assessment_target(self, resourceGroupArn: str):
        '''2nd step'''
        resp = self.inspector.create_assessment_target(assessmentTargetName=self.targetAssessmentName,
                                                       resourceGroupArn=resourceGroupArn)
        return resp['assessmentTargetArn']

    def create_assessment_template(self, assessmentTargetArn: str, durationInSeconds=300, assessmentTemplateName=f"Default_Template_Name"):
        '''3rd step'''
        resp = self.inspector.create_assessment_template(
            assessmentTargetArn=assessmentTargetArn,
            assessmentTemplateName=assessmentTemplateName,
            durationInSeconds=durationInSeconds,
            rulesPackageArns=self.rule_arns)
        return resp['assessmentTemplateArn']

    def start_assesment_run(self, assessmentTemplateArn: str, \
         unique_assesment_name="Default_Assesment_Name"):
        '''4th step'''
        resp = self.inspector.start_assessment_run(assessmentTemplateArn=assessmentTemplateArn,
                                                   assessmentRunName=unique_assesment_name)
        return resp['assessmentRunArn']

    def stop_assessment_run(self, assessmentRunArn: str):
        '''5th step'''
        resp = self.inspector.stop_assessment_run(
            assessmentRunArn=assessmentRunArn,
            stopAction='START_EVALUATION')

    def get_assessment_report(self, assessmentRunArn):
        '''6th step'''
        resp = self.inspector.get_assessment_report(
            assessmentRunArn=assessmentRunArn,
            reportFileFormat='HTML',
            reportType='FULL'
        )

        return resp

def lambda_handler(event,context):
    rule = {rule_package_key: rule_package_value}
    ig = InspectorGadget('InspectorGadget', rule )
