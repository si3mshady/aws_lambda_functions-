from simple_salesforce import Salesforce
import os 

accessToken = os.getenv('TOKEN')
password = os.getenv('PASSWORD')
username =  os.getenv('USERNAME')

def forceBeWithYou():
    return Salesforce(username=username, password=password,security_token=accessToken)

def customerDialInNumber(event):
    cust_phone =  event['Details']['ContactData']['CustomerEndpoint']['Address']
    return cust_phone

def create_new_contact(event):
    cust_desired_contact = event['Details']['Parameters']['StoredCustomerInput']
    contact_id = event['Details']['Parameters']['ContactID']
    sForce = forceBeWithYou()
    if cust_desired_contact != customerDialInNumber(event):
        res = sForce.Contact.create({'LastName':"JDoe-" + contact_id,'LeadSource':contact_id,'MobilePhone':cust_desired_contact,'OtherPhone': customerDialInNumber(event)})
    else:
        res = sForce.Contact.create({'LastName':"JDoe-" + contact_id,'LeadSource':contact_id,'MobilePhone':cust_desired_contact})   
    
    return res['success']


def lambda_handler(event,context):
    try:    
        if create_new_contact(event):      
            return {
                "Message": "A new record was created in salesforce"
            }
        else:
            return {
                "Message": "There was an error. No data was created in salesforce"
            } 
    except:
        pass
        

#AWS Connect Salesforce Lambda IVR practice 
#Create Contact Flow Retrieve Customer infomation use to create salesforce user
#Elliott Arnold DMS DFW Covid-19  11-13-20 
#lateNightToil BuringTheMidnightOil 
