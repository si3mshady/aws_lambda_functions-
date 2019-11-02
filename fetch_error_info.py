import wget, time
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


class TroubleShoot_Exceptions:
    @classmethod
    def init_driver(cls):
        url = "https://www.google.com"
        driver = Firefox(executable_path="/Users/si3mshady/geckodriver")
        driver.get(url)
        driver.implicitly_wait(4)
        return driver

    @classmethod
    def simulate_exception(cls):
        exception = cls.throw_exception()
        cls.clarify_exception(exception)

    @classmethod
    def throw_exception(cls):
        value='x'
        try:
            int(value) + int(value)
        except Exception as e:
            return str(e)

    @classmethod
    def clarify_exception(cls,exception: str):
        driver = cls.init_driver()
        try:
            driver.find_element(By.XPATH, "//input[@type='text']").send_keys(exception)
            driver.find_element(By.XPATH, "//ul//li[1]").click()
            target = driver.find_element(By.XPATH, "(//h3[@class='LC20lb']/parent::a[@href])[1]")
            driver.execute_script("arguments[0].click();",target)
            time.sleep(5)
            print(driver.current_url)
            wget.download(url=driver.current_url, out='exception-troubleshooting-' + str(round(time.time() * 1000)))
            driver.close()
        except (NoSuchElementException, ElementNotInteractableException):
            driver.find_element(By.XPATH, "//input[@type='text']").click()
            driver.find_element(By.XPATH, "(//h3[@class='LC20lb']/parent::a[@href])[1]").click()
            time.sleep(5)
            print(driver.current_url)
            wget.download(url=driver.current_url, out='exception-troubleshooting-' + str(round(time.time() * 1000)))
            driver.close()
        finally:
            driver.quit()

#Selenium Practice - learning to traverse the DOM with xpath
#Utility Class to be used alongside troubleshooting exceptions
#Once configured the script will preform a search and download of the most relevant article to resolve the issue.
#Elliott Arnold 11-2-19
#si3mshady





