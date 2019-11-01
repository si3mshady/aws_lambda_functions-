from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import wget

class SEC:

    def __init__(self,cik=None):
        self.driver = self.set_init_driver()
        self.cik = cik if cik else input(str("Please enter a new CIK value to search: "))

    #instance method
    def set_init_driver(self):
        ff_driver = "/Users/si3mshady/PycharmProjects/Learning_Selenium_WebDriver/drivers/geckodriver"
        url = "https://www.sec.gov/edgar/searchedgar/companysearch.html"
        driver = webdriver.Firefox(executable_path=ff_driver)
        driver.get(url)
        driver.implicitly_wait(3)
        return driver

    #instance method
    def fetch10K(self):
        try:
            self.driver.find_element(By.XPATH, "//input[@id='cik']").send_keys(self.cik)
            self.driver.find_element(By.XPATH, "//input[@id='cik_find']").click()
            self.driver.find_element(By.XPATH,"//td[contains(text(),'Annual report')]/preceding-sibling::td//a[@id='documentsbutton' and @href]").click()
            self.driver.find_element(By.XPATH,"//td[contains(text(),'10-K')]/following-sibling::td//a").click()
            wget.download(self.get_current_url())
            print(str(self.get_current_url() + ' is downloaded'))
        except NoSuchElementException:
            print('No items found')

    #instance method
    def get_current_url(self):
        return self.driver.current_url

    @classmethod
    def set_init_driver(cls):
        ff_driver = "/Users/si3mshady/PycharmProjects/Learning_Selenium_WebDriver/drivers/geckodriver"
        url = "https://www.sec.gov/edgar/searchedgar/companysearch.html"
        driver = webdriver.Firefox(executable_path=ff_driver)
        driver.get(url)
        driver.implicitly_wait(3)
        return driver

    @classmethod
    def fetchMultiple10K(cls,*civ):
        civ_list = civ

        for i, _ in enumerate(civ_list):
            try:

                print('Sending CIV:  ' + civ_list[i])

                cls.driver = cls.set_init_driver()
                cls.driver.find_element(By.XPATH, "//input[@id='cik']").send_keys(civ_list[i])
                cls.driver.find_element(By.XPATH, "//input[@id='cik_find']").click()
                cls.driver.find_element(By.XPATH,"//td[contains(text(),'Annual report')]/preceding-sibling::td//a[@id='documentsbutton' and @href]").click()
                cls.driver.find_element(By.XPATH, "//td[contains(text(),'10-K')]/following-sibling::td//a").click()
                wget.download(cls.get_current_url())
                print(str(cls.get_current_url() + ' is downloaded'))
            except NoSuchElementException:
                print('No items found')

    @classmethod
    def get_current_url(cls):
        return cls.driver.current_url



#Web Driver Practice: Learning Selenium Web Automation - xpath exercices navigating the DOM
#Fetching 10K forms from sec.gov
#Elliott Arnold
#Happy Halloween
#10-31-19




#https://sqa.stackexchange.com/questions/32097/how-to-find-xpath-inside-td
#https://selenium-python.readthedocs.io/locating-elements.html
#https://navyuginfo.com/preceding-sibling-following-sibling-xpath/
