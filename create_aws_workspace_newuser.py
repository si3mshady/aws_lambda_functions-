import json, time, boto3, subprocess, os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

sm = boto3.client('secretsmanager', region_name='us-east-1')
secrets = sm.get_secret_value(SecretId='login').get('SecretString')
secrets = json.loads(secrets)


def handler(event):

    username = event[0]  
    firstName = event[1]
    lastName = event[2]
    email = event[3]                             
      
        
    options = Options()
    options.add_argument("--start-maximized") 
    options.binary_location = '/usr/bin/google-chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080') #needed to prevent object is not clickable error 
   
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver',chrome_options=options)
    driver.maximize_window()
    driver.implicitly_wait(14)
    
    driver.get('https://530182258888.signin.aws.amazon.com/console')
    driver.get('https://console.aws.amazon.com/workspaces/home?region=us-east-1#listworkspaces')
   
    iam_user_field_xpath = '//*[@id="username"]'
    driver.find_element(By.XPATH, iam_user_field_xpath).send_keys(secrets.get('Username'))

    password_xpath = '//*[@id="password"]'
    driver.find_element(By.XPATH, password_xpath).send_keys(secrets.get('Password'))

    login_xpath = '//*[@id="signin_button"]'
    driver.find_element(By.XPATH, login_xpath).click()    

    
    launch_workspace_button = '//*[@id="workspacesAddNewUsersButton"]'
    time.sleep(6)
    button = driver.find_element(By.XPATH, launch_workspace_button)
    print(button)
    button.click()
    
    time.sleep(6)
    
    next_button_xpath = ' //*[@id="nextButtonId"]'
   

    next_button = driver.find_element(By.XPATH, next_button_xpath)
    print(next_button)
    next_button.click()   


    username_xpath =  '//*[@id="c"]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[5]/div/div[2]/div[2]/div/table/tbody/tr/td[1]/div/input'
    firstName_xpath = '//*[@id="c"]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[5]/div/div[2]/div[2]/div/table/tbody/tr/td[2]/div/input'
    lastName_xpath = '//*[@id="c"]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[5]/div/div[2]/div[2]/div/table/tbody/tr/td[3]/div/input'
    email_xpath = '//*[@id="c"]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[5]/div/div[2]/div[2]/div/table/tbody/tr/td[4]/div/input'
    
    driver.find_element(By.XPATH, username_xpath).send_keys(username)
    driver.find_element(By.XPATH, firstName_xpath).send_keys(firstName)
    driver.find_element(By.XPATH, lastName_xpath).send_keys(lastName)
    driver.find_element(By.XPATH, email_xpath).send_keys(email)

    create_user_xpath = '//*[@id="identifyUsersCreateUsersButton"]'

    driver.find_element(By.XPATH, create_user_xpath).click()

    print('done')

    driver.quit()

    return { "status": 200, "message": "success"}
    
if __name__== '__main__':    

    #get command line arguments 
    entries = [entry for entry in sys.argv[1:]]    


    if len(entries) != 4:
        print('Not enough arguments to create user')
        exit()

    handler(entries)
