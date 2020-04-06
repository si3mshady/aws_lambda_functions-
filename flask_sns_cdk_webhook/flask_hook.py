from flask import Flask, request
from flask_restful import Resource, Api
import subprocess

app=application=Flask(__name__)
api=Api(app)

class CaptainHook(Resource):
    def post(self):
        data = request.data
        cmd = 'sudo docker run -itv $(pwd):/cdk  si3mshady/cdk-ec2-iam cdk deploy'
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

api.add_resource(CaptainHook,'/hook')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

