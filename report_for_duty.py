from selenium import webdriver
from selenium.webdriver.common.by import By


#init 
chrome_driver = '/Users/e/automation/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_driver)
driver.get("https://aws.amazon.com/")
driver.implicitly_wait(8)

#select my account from drop down 
drop_down_xpath = '//*[@id="m-nav"]/div[1]/div[2]/a[4]'
dd  = driver.find_element(By.XPATH,drop_down_xpath)
dd.click()

#select drop down 
console_xpath = "/html/body/div[6]/ul/li[1]/a"
console_link = driver.find_element(By.XPATH,console_xpath)
console_link.click()

#enter login email 
input_xpath = '//*[@id="resolving_input"]'
email_input = driver.find_element(By.XPATH,input_xpath)
email_input.send_keys('elliott@arnold.com')

#select next btn 
next_btn_xpath = '//*[@id="next_button"]'
next_btn = driver.find_element(By.XPATH,next_btn_xpath)
next_btn.click()

#enter pw 
pw_xpath = '//*[@id="password"]'
pw_input = driver.find_element(By.XPATH,pw_xpath)
pw_input.send_keys("elliottsPassword")

#submit pw 
btn_submit_xpath = '/html/body/div[1]/div[2]/div[1]/div[1]/div[3]/div[5]/button'
sign_in = driver.find_element(By.XPATH,btn_submit_xpath)
sign_in.click()

#popluate input search field 
console_input_xpath = '//*[@id="search-box-input"]'
find_services = driver.find_element(By.XPATH,console_input_xpath)
find_services.send_keys('api gateway')

#select apigateway from drop down  
apigw_xpath  = '//*[@id="search-box-input-dropdown-ag"]/awsui-select-option/div/div/div[1]'
apigw = driver.find_element(By.XPATH,apigw_xpath)
apigw.click()

#AWS Python3 Console Selenium Automation - Sign in for the day - Select ApiGateway 
#Elliott Arnold 9-17-2020  AWS DMS DFW Amazonian 
#Quick and Dirty / Covid19
