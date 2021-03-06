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
This package is used to query DynamoDB
'''
from __future__ import print_function
from boto3 import resource
from boto3.dynamodb.conditions import Key
import decimal
import json

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class DynamoRepository:
    
    def __init__(self, target_dynamo_table, region='eu-west-1'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.dynamo_table = target_dynamo_table
        self.table = self.dynamodb.Table(self.dynamo_table)

    def query_dynamo_record_by_parition(self, parition_key, parition_value):
        try:
            response = self.table.query(
                        KeyConditionExpression=Key(parition_key).eq(parition_value))
            for record in response.get('Items'):
                print(json.dumps(record, cls=DecimalEncoder))
            return
            
        except Exception as e:            
            print(e.__doc__)
            print(e.message)
    
    def query_dynamo_record_by_parition_sort_key(self, parition_key, parition_value, 
                                                 sort_key, sort_value): 
        try:
            response = self.table.query(
                        KeyConditionExpression=Key(parition_key).eq(parition_value)  
                        & Key(sort_key).gte(sort_value))
            for record in response.get('Items'):
                print(json.dumps(record, cls=DecimalEncoder))
            return
            
        except Exception as e:            
            print(e.__doc__)
            print(e.message)
        
def main():
    
    table_name = 'poc-lambda-user-visits'
    parition_key = 'EventId'
    parition_value = '' 
    sort_key ='EventDay'
    sort_value = 20171014
    
    dynamoRepo = DynamoRepository(table_name)
    print('Reading all data for user:%s'%parition_value)
    dynamoRepo.query_dynamo_record_by_parition(parition_key,parition_value)
    
    print('Reading all data for user:%s with date > %d'%(parition_value,sort_value))
    dynamoRepo.query_dynamo_record_by_parition_sort_key(parition_key,
                                                        parition_value, 
                                                        sort_key, 
                                                        sort_value)


if __name__ == '__main__':
    main()