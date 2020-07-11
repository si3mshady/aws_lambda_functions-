#step 1 create vpc link - must have network load balancer => 'target-arn'
aws apigateway create-vpc-link --name tgif \
	--target-arns arn:aws:elasticloadbalancing:us-east-:*:loadbalancer*

#step 2 get json response - id = connection-id of VPC LINK
{
    "id": "888888",
    "name": "tgif",
    "targetArns": [rn:aws:elasticloadbalancing:us-east-:*:loadbalancer*],
    "status": "PENDING"
}

#Step 3 execute method integration command 
aws apigateway put-integration \
        --region us-east-1 \
        --rest-api-id 3pq5**** \   #located from API Dashboard - Name,Description,ID
        --resource-id lw**** \     #ID of Endpoint resource - 6 digit number located in navigation bar of API gateway console 
        --http-method ANY \
        --connection-type VPC_LINK \
        --connection-id 888888 \    #Connection Id generated from step 2
        --integration-http-method  ANY \
        --type HTTP_PROXY \
        --uri https://www.testing123.com
        
#Step 4 check json response 
{
    "type": "HTTP_PROXY",
    "httpMethod": "ANY",
    "uri": "https://www.testing123.com",
    "connectionType": "VPC_LINK",
    "connectionId": "888888",
    "passthroughBehavior": "WHEN_NO_MATCH",
    "timeoutInMillis": 29000,
    "cacheNamespace": "lw****",   #same as resource id 
    "cacheKeyParameters": []
}
