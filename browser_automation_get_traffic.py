from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import boto3



class Traffic:

    def __init__(self, url=''):
        self.ses = boto3.client('ses')
        self.ff_driver = "/Users/si3mshady/PycharmProjects/Learning_Selenium_WebDriver/drivers/geckodriver"
        self.url = url
        self.driver = self.set_init_driver()

    def set_init_driver(self):
        driver = webdriver.Firefox(executable_path=self.ff_driver)
        driver.get(self.url)
        driver.implicitly_wait(3)
        return driver

    def get_situational_awareness(self):
        '''enter search query, click search button, click png image, take screenshot save to file'''
        self.xpath_input = "/html/body/div/div[4]/form/div[2]/div[1]/div[1]/div/div[2]/input"
        self.input_field = self.driver.find_element(By.XPATH, self.xpath_input)
        self.input_field.send_keys("traffic dallas texas")
        self.xpath_search_buttton = "/html/body/div/div[4]/form/div[2]/div[1]/div[3]/center/input[1]"
        self.search_button = self.driver.find_element(By.XPATH, self.xpath_search_buttton)
        self.search_button.click()
        button = "/html/body/div[6]/div[3]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/div[2]/a"
        self.search_button = self.driver.find_element(By.XPATH, button).click()
        save_as = "/Users/si3mshady/PycharmProjects/Learning_Selenium_WebDriver/Selenium_Practice/traffic.png"
        self.driver.save_screenshot(save_as)
        self.send_email()

    def send_email(self):
        '''documentation = https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html '''
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = 'traffic'
        msg['From'] = 'si3mshady@gmail.com'
        msg['To'] = 'alquimista2891@gmail.com'

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(open('traffic.png', 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename="traffic.png")

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        msg.attach(att)
        # print(msg)
        response = self.ses.send_raw_email(
                Source='alquimista2891@gmail.com',
                Destinations=[
                    'si3mshady@gmail.com'
                ],
                RawMessage={
                    'Data': msg.as_string(),
                }
            )


#AWS SES, Selenium practice: taking screenshots
#Small class/exercise created to practice locating items from the DOM using xpath
#Class generates a screenshot of current traffic conditions and sends to authorized email configured with SES
#Elliott Arnold 10-45-19
#si3mshady

#e = Traffic("https://www.google.com/")
#e.get_situational_awareness()










































#https://medium.com/@codelovingyogi/sending-emails-using-aws-simple-email-service-ses-220de9db4fc8