'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 8 Jan 2018

@author: Richard Freeman

pip install boto3

This package creates a new DynamoDb table with the specified read and write capacity

'''
from __future__ import print_function
import boto3

def create_dynamo_lambda_counters_table(tableNameValue, enableStreams=False,
                                                     readCapacity=100,
                                                     writeCapacity=50, 
                                                     region='eu-west-1'):
    table_name = tableNameValue
    print('creating table: ' + table_name)  
    try:
        client=boto3.client(service_name='dynamodb', region_name=region)
        print (client.create_table(TableName=table_name,
              AttributeDefinitions=[{'AttributeName': 'EventId',
                                    'AttributeType': 'S'},
                                    {'AttributeName': 'EventDay',
                                    'AttributeType': 'N'}],
              KeySchema=[{'AttributeName': 'EventId',
                          'KeyType': 'HASH'},
                         {'AttributeName': 'EventDay',
                          'KeyType': 'RANGE'},
                         ],                    
              ProvisionedThroughput={'ReadCapacityUnits': readCapacity, 'WriteCapacityUnits': writeCapacity}))
    except Exception as e:
        print(str(type(e)))             
        print(e.__doc__)
        print(e.message)

def main():
    
    table_name = 'poc-lambda-user-visits'
    create_dynamo_lambda_counters_table(table_name, True, 2, 1)
    

if __name__ == '__main__':
    main()