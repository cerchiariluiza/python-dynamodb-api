'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 31 Dec 2017

@author: Richard Freeman

'''
import json
from lambda_dynamo_get import lambda_return_all_parameters as lambda_all_params
from lambda_dynamo_get import lambda_return_dynamo_records as lambda_query_dynamo

with open('../sample_data/request-api-gateway-valid-date.txt', 'r') as file:
    event=json.loads(file.read()) 
print("lambda_all_params\nUsing data: " + str(event))
print(file.name.split('/')[-1])
response = lambda_all_params.lambda_handler(event, None)
print("Response: %s \n"% json.dumps(response))

print("lambda_query_dynamo\nUsing data: " + str(event))
print(file.name.split('/')[-1])
response = lambda_query_dynamo.lambda_handler(event, None)
print("Response: %s\n"% json.dumps(response))

with open('../sample_data/request-api-gateway-valid-no-date.txt', 'r') as file:
    event=json.loads(file.read()) 
print(file.name.split('/')[-1])
print("lambda_query_dynamo\nUsing data: " + str(event))
response = lambda_query_dynamo.lambda_handler(event, None)
print("Response: %s\n"% json.dumps(response))

with open('../sample_data/request-api-gateway-error.txt', 'r') as file:
    event=json.loads(file.read()) 
print(file.name.split('/')[-1])
print("lambda_query_dynamo\nUsing data: " + str(event))
response = lambda_query_dynamo.lambda_handler(event, None)
print("Response: %s\n"% json.dumps(response))
