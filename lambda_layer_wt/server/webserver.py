import os, subprocess, time, shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory

flask_app = app = Flask(__name__, static_folder='../build', static_url_path='/')

def makeScratchSpace():
    try: 
        os.makedirs(str(Path.home()) + '/lambdaLayerScratchSpace')        
    except FileExistsError:
        pass

def removeScratchDir():
    path = str(Path.home()) + '/lambdaLayerScratchSpace'
    shutil.rmtree(path) 


def downloadPackages(runtime, package, fullPath, zipName,s3Bucket): 

    if "python" in runtime.lower():        
        cmd = f'pip3 install {package} -t {fullPath}'
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(8)
        zipAndSendToS3(zipName,fullPath,s3Bucket)
    if "node" in runtime.lower():
        
        cmd = f'npm install  --prefix {fullPath} {package}'        
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(8)
        zipAndSendToS3(zipName,fullPath,s3Bucket)
        

def makeCompatibleDirs(runtime, package, packageNameZip, s3Bucket):
    basePath = str(Path.home()) + '/lambdaLayerScratchSpace/'
    if runtime.lower() == 'python3.8':
        fullPathToSitePackages = basePath + "python/lib/python3.8/site-packages/"        
        try:            
            os.makedirs(fullPathToSitePackages)   
            downloadPackages(runtime,package,fullPathToSitePackages, packageNameZip, s3Bucket)         
        except FileExistsError:
             downloadPackages(runtime,package,fullPathToSitePackages, packageNameZip, s3Bucket)
            
    if runtime.lower() == 'python3.7':
        fullPathToSitePackages = basePath + "python/lib/python3.7/site-packages/"
        try:            
            os.makedirs(fullPathToSitePackages)           
            downloadPackages(runtime,package,fullPathToSitePackages, packageNameZip, s3Bucket)
        except FileExistsError:
            downloadPackages(runtime,package,fullPathToSitePackages, packageNameZip, s3Bucket)
           
    if runtime.lower() == 'node':
        fullPathToSitePackages = basePath + "nodejs/"
        try:            
            os.makedirs(fullPathToSitePackages)    
            downloadPackages(runtime,package,fullPathToSitePackages, packageNameZip, s3Bucket)                    
        except FileExistsError:
            downloadPackages(runtime,package,fullPathToSitePackages, packageNameZip, s3Bucket)

def zipAndSendToS3(zipName,fullPathToDir,s3Bucket):    
    #remove homeDirectory + ScratchDirectory from path, must use relative path to create zip  
    pathToZip = fullPathToDir.split('/')[4:]
    #split into an array
    #join array replcaing '' with, '/'
    pathToZip = '/'.join(pathToZip)
    print('pathTozip stage3',pathToZip)
    cd_cmd = 'cd' + ' ' +  str(Path.home()) + '/lambdaLayerScratchSpace;'
    # cmd = f'zip -r {zipName}' + ' ' +  '/'.join(pathToZip.split('/')[:4]) +  ';'
    cmd = f'zip -r {zipName}' + ' ' +  pathToZip  + ';'
    fullCommand = cd_cmd + cmd
    res = subprocess.Popen(fullCommand, stdout=subprocess.PIPE, shell=True)
    #create output from zip command 
    res.communicate()
    time.sleep(12)
    path = str(Path.home()) + '/lambdaLayerScratchSpace/'
    cmd2 = f'aws s3 cp {path}{zipName} s3://{s3Bucket}'
    subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
    time.sleep(10)
    removeScratchDir()


@flask_app.route('/', methods=['GET','POST'])
def index():    
    
    makeScratchSpace()
    try:
        runtime = request.args['runtime']
        packageNameZip = request.args['packageNameZip']
        s3Bucket = request.args['s3Bucket']
        module = request.args['module']
        makeCompatibleDirs(runtime, module, packageNameZip, s3Bucket)
    except KeyError:
        pass

    return app.send_static_file('index.html')


if __name__ == '__main__':
    flask_app.run(host='localhost', debug=True, port=os.environ.get('PORT', 8080))

#AWS Lambda, S3, React Flask  - basic Lambda Layers creation tool
#Use small webform to generate deployment package needed for simple lambda layer - send to s3 
#Elliott Arnold  - DMS 
#1-3-2021 mi cumpleanos 