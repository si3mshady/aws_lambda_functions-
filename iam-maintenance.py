from dateutil.tz import tzutc
from datetime import datetime
import boto3

class IAM_Maintenance():

    def __init__(self,numDaysFromCreatedDate=90,lastAuthenticationThreshold=90,agedAccessKeyThreshold=90):
        self.iam = boto3.client('iam')
        self.inactiveDays = numDaysFromCreatedDate
        self.lastAuthThreshold = lastAuthenticationThreshold
        self.agedAccessKey = agedAccessKeyThreshold

    def fetchIAMUsers(self):
        return [username['UserName'] for username in self.iam.list_users()['Users']]

    def checkAgedAccessKeys(self):
        '''creates generator of all users with aged (x) access keys'''
        for _ ,user in enumerate(self.fetchIAMUsers()):
            createDate = self.iam.list_access_keys(UserName=user)['AccessKeyMetadata'][0]['CreateDate']
            delta = datetime.now(tzutc()) - createDate
            if delta.days > self.agedAccessKey:
                yield (user)

    def fetchAgedRoles(self):
        '''if tzutc is not set, method will throw TypeError exception:
        can't subtract offset-naive and offset-aware datetimes'''
        self.roles = self.iam.list_roles()
        for index, record in enumerate(self.roles['Roles']):
            createdDate = self.roles['Roles'][index]['CreateDate']
            deltaTime = datetime.now(tzutc()) - createdDate
            if deltaTime.days > self.inactiveDays:
                try:
                    if self.checkLastAuthenticationDate(record['RoleName'],record['Arn']):
                        yield(record['RoleName'])
                except KeyError:
                    pass

    def checkLastAuthenticationDate(self,roleName,arn):
        '''check when an IAM resource (user, group, role, or policy)
        was last used in an attempt to access AWS services '''
        job_id = self.iam.generate_service_last_accessed_details(Arn=arn)['JobId']
        last_authenticated_date = self.iam.get_service_last_accessed_details(JobId=job_id)['ServicesLastAccessed'][0]['LastAuthenticated']
        delta = datetime.now(tzutc()) - last_authenticated_date
        if delta.days > self.lastAuthThreshold:
            return True

#AWS IAM Administration exercise: created basic class to help determine aging IAM resources (roles and user access)
#Elliott Arnold 10-13-19
#late night toil burning the midnight oil


