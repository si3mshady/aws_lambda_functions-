from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from functools import wraps
import time, os , boto3, wget


def queueItUp(func):
    '''decorator will create sqs queue if does not exist.'''
    @wraps(func)
    def wrapper(*args):
        try:
            sqs = boto3.client('sqs')
            res_downloaded = sqs.create_queue(QueueName='Downloaded')
            res_error = sqs.create_queue(QueueName='Error')
            with open('QueueUrls.txt','w') as ink:
                ink.write(res_downloaded['QueueUrl'] + '\n')
                ink.write(res_error['QueueUrl'] + '\n')
        except:
            pass
        result = func(*args)
        return result
    return wrapper


def makeDir(func):
    '''decorator will create a directory if does not exist.'''
    @wraps(func)
    def container(*args):
        try:
            if not os.path.exists('./linkedIn'):
                os.mkdir('./linkedIn')
            result = func(*args)
        except FileExistsError as e:
            print(e)
        return result
    return container

class LinksOnLinksOnLinks:
    @classmethod
    def init_driver(cls):
        '''If private browsing is not set, linkedin prompts for a login'''

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        url = 'https://www.linkedin.com/feed/'
        driver = Firefox(executable_path="/Users/si3mshady/geckodriver",firefox_profile=firefox_profile)
        driver.get(url)
        driver.implicitly_wait(5)
        return driver

    @classmethod
    @queueItUp
    @makeDir
    def init(cls):
        cls.sqs = boto3.client('sqs')
        driver = cls.init_driver()
        creds = [cred.strip() for cred in open('creds.txt').readlines()]
        #created with queueItUp Decorator
        queue = [queue.strip() for queue in open('QueueUrls.txt').readlines()]

        try:
            driver.find_element(By.XPATH,"//a[@class='sign-in-link']").click()
        except NoSuchElementException:
            driver.find_element(By.XPATH, "//a[@class='main__sign-in-link']").click()


        username = driver.find_element(By.XPATH,"//input[@id='username']")
        username.send_keys(creds[0])

        password = driver.find_element(By.XPATH, "//input[@id='password']")
        password.send_keys(creds[1])


        submit = driver.find_element(By.XPATH,"//button[@type='submit']")
        submit.click()

        saved = driver.find_element(By.XPATH,"//a[@href='/feed/saved/']")
        saved.click()

        articles = driver.find_element(By.XPATH, "//button[@aria-label='Articles']")
        articles.click()

        try:
            while True:
                links = driver.find_elements(By.XPATH,"//div[@class='core-rail']//a[@class='feed-shared-article__meta flex-grow-1 full-width tap-target app-aware-link ember-view' and @href]")

                '''Articles are downloaded to ./linkedIn directory created with 
                decorator, if successfull the url for the download is sent to the 'Downloaded' sqs queue.
                If unsuccessful the url is sent to 'Error' sqs queue'''

                for i in links:
                    try:
                        print(i.get_attribute("href"))
                        wget.download(i.get_attribute("href"), './linkedIn')
                        cls.sqs.send_message(QueueUrl=queue[0], MessageBody=str(i.get_attribute("href")))
                        print(i.get_attribute("href") + 'has been downloaded & url sent to Downloaded queue')

                    except Exception:
                        print(i.get_attribute("href") + 'was not downloaded & url sent to Error queue')
                        cls.sqs.send_message(QueueUrl=queue[1], MessageBody=str(i.get_attribute("href")))

                #click 3 dot icon
                driver.find_element(By.XPATH, "(//li-icon[@aria-label='Open control menu'])[1]").click()

                #￿click to unsave
                driver.find_element(By.XPATH,"(//span[@class='feed-shared-control-menu__headline t-14 t-black t-bold'])[1]").click()

                time.sleep(2)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        except Exception as e:
            print(e)


LinksOnLinksOnLinks.init()

#Selenium - LinkedIn - Python Practice
#Using selenium to retrieve all saved articles from saved pages
#Updated with Decorators, Boto3 and Wget - Unsaves Article
#Elliott Arnold
#11-12-19
#fin
