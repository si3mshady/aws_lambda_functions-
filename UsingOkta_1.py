import requests

#Needed for OauthFlow Needed for Oauth2Flow 
def getAuthCodeFromCallBack(oktaDomain,clientID,redirectUri):
    #url needed to start Oauth2 flow in order to recieve
    #uthCode returned in url, authcode is needed to retrieve JWT
    return  f'https://{oktaDomain}/oauth2/' \
    + f'default/v1/authorize?client_id={clientID}'\
    + f'&response_type=code&scope=openid&'\
      + f'redirect_uri={redirectUri}&state=si3mshady&nonce=888'

def getOktaJWT(oktaDomain,clientID,clientSecret,redirectUrl,AuthCode):
    #jwt identifies a user 
    url = f'https://{oktaDomain}/oauth2/default/v1/token'
	payload = {"client_id":{clientID},"client_secret":clientSecret,"grant_type":"authorization_code",\
        "redirect_uri":redirectUrl,"code":AuthCode}
	r1 = requests.post(url, data=payload)
    if r1.status_code ==  200:
        return r1.json()['access_token']
    else:
        print(res)
        print(res.text)
    

def loginGetSesionToken(oktaDomain,username,password):
    # https://realpython.com/python-requests/#the-message-body
    url = f"https://{oktaDomain}/api/v1/authn"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}   
    #if you use data parameter you will get 400 The request body was not well-formed 
    res = requests.post(url,headers=headers,json={"username":username,  "password": password})
    if res.status_code == 200:
        print(res)    
        return res.json()['sessionToken']
    else:
        print(res) 
        print(res.text)

def getLogs(oktaDomain, application_api_token):
    url = f"https://{oktaDomain}/api/v1/logs"
    headers = {"Accept": "application/json","Content-Type": "application/json", "Authorization": f"SSWS {application_api_token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
         print(res)
         print(res.text)
         postToSIEM(res.text)
         return res.json()
    else:
        print(res)
        print(res.text)


def postToSIEM(data,siem_endpoint=''):
    siem_endpoint = "https://hvyjotibx6.execute-api.us-east-1.amazonaws.com/v1/siemdata"
    res = requests.post(url=siem_endpoint, data=data)
    if res.status_code == 200:
        print(f"Data posted successfully to {siem_endpoint}")
    else:
        print(res)
        print(res.text)
        print(f"Data post unsuccessfull")



#AWS Okta IdentityProvider Requests
#Okta Identity 

# https://developer.okta.com/docs/reference/
#https://developer.okta.com/docs/reference/api/system-log/#examples
#/https://devforum.okta.com/t/how-to-login-to-okta-and-access-an-app-using-python-for-automation-purpose/11171
# https://www.w3schools.com/python/ref_requests_response.asp
