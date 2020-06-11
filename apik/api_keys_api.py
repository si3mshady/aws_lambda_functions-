from api_key_wrapper import (KeyManagment, get_username_email, update_usage_plan)
from flask import Flask, request
from flask_restful import Resource,Api
import boto3


app=application=Flask(__name__)
api=Api(app)


class NewApiKey(Resource):
    def post(self):        
        data = request.get_json()
        username = data['username']
        email = data['email']
        get_username_email(username,email)
        update_usage_plan(email)               
        json_response = {
            "status": 200,
            "message": f"Thank you for registering,{username}, " + \
                 "your API KEY will be sent to you in a seperate email."
        }
        return json_response

api.add_resource(NewApiKey,'/new_key')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 


#AWS API Gateway Dynamo DB Usage API Key practice
#Create simple decorators to work with flask API
#Decorators provide additional functionality to methods
#When used, decorators generate api keys, updates DynamoDb table and 
#assign api key to usage plan for use with authentication
#Elliott Arnold 6-11-20 