import selenium, os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart



class TrafficJam:
    @classmethod
    def init_driver(cls):
        driver_location = '/usr/bin/chromedriver'
        os.environ['webdriver.chrome.driver'] = driver_location

        options = Options()
        options.headless = True

        driver = selenium.webdriver.Chrome(driver_location, options=options)
        url = 'http://its.txdot.gov/dal/dal.htm'
        driver.implicitly_wait(8)
        driver.get(url)
        return driver

    @classmethod
    def traffic_report(cls):
        '''fetch traffic data from TXDot'''
        driver = cls.init_driver()
        driver.fullscreen_window()
        driver.find_element(By.XPATH, "//a[@href and contains(text(),'Incidents')]").click()
        time.sleep(8)
        driver.save_screenshot('Incidents.png')
        cls.send_email('Incidents.png')

        driver.find_element(By.XPATH, "//a[@href and @id='tab6Link']").click()
        time.sleep(8)
        driver.save_screenshot('TravelTimes.png')
        cls.send_email('TravelTimes.png')


    @classmethod
    def send_email(self, filename):
        ses = boto3.client('ses',region_name='us-east-1')
        '''documentation = https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html '''
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = 'Traffic_Report'
        msg['From'] = 'si3mshady@gmail.com'
        msg['To'] = 'alquimista2891@gmail.com'

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Define the attachment part and encode it using MIMEApplication.
        att = MIMEApplication(open(filename, 'rb').read())

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        att.add_header('Content-Disposition', 'attachment', filename=filename)

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)

        # Add the attachment to the parent container.
        msg.attach(att)
        print('Sending email')
        response = ses.send_raw_email(
                Source='si3mshady@gmail.com',
                Destinations=[
                    'alquimista2891@gmail.com'
                ],
                RawMessage={
                    'Data': msg.as_string(),
                }
            )

TrafficJam.traffic_report()



#AWS/EC2/Selenium - Practice: Using Chrome Browserless Mode on EC2 to fetch traffic screenshots
#Elliott Arnold  11-15-19

#https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
#https://chromedriver.chromium.org/getting-started
#https://www.parrotqa.com/selenium-tutorial