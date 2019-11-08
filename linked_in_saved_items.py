from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class LinksOnLinksOnLinks:
    @classmethod
    def init_driver(cls):
        '''If private browsing is not set, youtube prompts for a login'''

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        url = 'https://www.linkedin.com/feed/'
        driver = Firefox(executable_path="/Users/si3mshady/geckodriver",firefox_profile=firefox_profile)
        driver.get(url)
        driver.implicitly_wait(5)
        return driver

    @classmethod
    def init(cls):
        driver = cls.init_driver()
        creds = [cred.strip() for cred in open('creds.txt').readlines()]

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

        while True:
            links = driver.find_elements(By.XPATH,"//div[@class='core-rail']//a[@class='feed-shared-article__meta flex-grow-1 full-width tap-target app-aware-link ember-view' and @href]")

            lol = open('lol.txt','a')
            for i in links:
                print(i.get_attribute("href"))
                lol.write(str(i.get_attribute("href") + '\n'))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            lol.close()

            time.sleep(10)


LinksOnLinksOnLinks.init()

#Selenium - LinkedIn - Python Practice
#Using selenium to retrieve all saved articles from saved pages
#Elliott Arnold
#11-7-19
#wip