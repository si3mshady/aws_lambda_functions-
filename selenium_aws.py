from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3


class Login():
    def login(self):
        ff_driver = "/Users/si3mshady/PycharmProjects/Learning_Selenium_WebDriver/drivers/geckodriver"

        with open('login_data.txt') as data:
            login_data = [x.strip() for x in data.readlines()]

        driver = webdriver.Firefox(executable_path=ff_driver)
        driver.get("https://aws.amazon.com/console/")
        xpath = "/html/body/header/div[1]/div[1]/div[2]/div/div/div/div/a"
        driver.find_element(By.XPATH, xpath).click()
        xpath = "/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div[6]/span/span/a"
        driver.find_element(By.XPATH, xpath).click()
        driver.find_element(By.XPATH, "//*[@id='resolving_input']").send_keys(login_data[0])
        driver.find_element(By.XPATH, "//*[@id='next_button']").click()
        driver.find_element(By.XPATH, "//*[@id='username']").send_keys(login_data[0])
        driver.find_element(By.XPATH, "//*[@id='password']").send_keys(login_data[1])
        driver.find_element(By.XPATH, "//*[@id='signin_button']").click()


class IAM_MFA(Login):

    def __init__(self, username):
        self.iam = boto3.client('iam')
        self.username = username

    def create_default_user(self):
        self.create_iam_user()
        self.attach_user_policy()
        self.create_user_login()
        self.add_user_to_group()
        self.create_virtual_mfa_device_qrc()

    def create_iam_user(self, tag_key=None,tag_value=None):
        '''first step'''

        response = self.iam.create_user(
            UserName=self.username,
            Tags=[
                {
                    'Key': tag_key if tag_key else self.username + "-key",
                    'Value': tag_value if tag_value else self.username + "-value"
                },
            ]
        )

        return response

    def attach_user_policy(self, policy_arn=None):
        '''second step'''
        '''set user policy - if no policy set - admin privileges
           for demonstration purposes '''

        response = self.iam.attach_user_policy(
            PolicyArn=policy_arn if policy_arn else "arn:aws:iam::aws:policy/AdministratorAccess",
            UserName=self.username
        )

        return response

    def create_user_login(self,password=None):
        '''third step'''
        '''set default password'''
        response = self.iam.create_login_profile(
            UserName=self.username,
            Password=password if password else self.username + "123!",
            PasswordResetRequired=True
        )

        return response

    def add_user_to_group(self, groupname=None):
        '''fourth step'''
        response = self.iam.add_user_to_group(
            GroupName=groupname if groupname else 'admin_group',
            UserName=self.username
        )

        return response

    def create_virtual_mfa_device_qrc(self, device_name=None):
        '''fifth step'''

        response = self.iam.create_virtual_mfa_device(VirtualMFADeviceName= device_name if device_name else self.username + "-virtual-device")
        with open(device_name if device_name else self.username + "qrc.png", 'wb') as code:
            code.write(response['VirtualMFADevice']['QRCodePNG'])

        self.serial = response['VirtualMFADevice']['SerialNumber']


    def enable_virtual_mfa_device(self,auth_code_1,auth_code_2):
        '''seventh step - requires google authenticator or equivalnt auth service'''
        response = self.iam.enable_mfa_device(
            UserName=self.username,
            SerialNumber=self.serial,
            AuthenticationCode1=auth_code_1,
            AuthenticationCode2=auth_code_2
        )

        return response




#AWS Boto3 - IAM - MFA - Selenium Practice:
#Created a class to create IAM users and set up MFA by generating QRC images
#Additionally, I am learning how to use Selenium Webdriver for website automation
#Using xpaths I am able to log into my aws account console  ￿
#Elliott Arnold 10-27-19
#si3mshady

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#virtualmfadevice
#https://blog.clearpathsg.com/blog/bid/306936/Setting-up-Multi-Factor-Authentication-with-Amazon-Web-Services-AWS