import pandas as pd
import boto3

apigw = boto3.client('apigateway')

#oneliner
res = pd.DataFrame({'ids': [i.get('id') for i in apigw.get_rest_apis().get('items')],'name': \
  [i.get('name') for i in apigw.get_rest_apis().get('items')]})

# >>> res
#           ids        name
# 0  xxjl5v9lsg  second api
# 1  ad5nzq58oj  fourth api
# 2  an5iwk2s98   third api
# 3  cs9o4b5hkg   first api

# >>> res.to_csv()

# ',ids,name\n0,55jl5v9lsg,second api\n1,ad5nzq58oj,fourth api\n2,an5iwk2s98,third api\n3,cs9o4b5hkg,first api\n'

#Elliott Arnold - prod notes from the field - 7-11 
#DevOps/Developer 1-9-21
