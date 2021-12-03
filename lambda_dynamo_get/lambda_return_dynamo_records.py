'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 30 Dec 2017
@author: Richard Freeman

This Lambda queries DynamoDB for a specific partition and greater than a
specific sort key.

'''
from __future__ import print_function
from boto3 import resource
from boto3.dynamodb.conditions import Key
import json
import decimal

def parse_parameters(event):
    try:
        returnParameters = event['queryStringParameters'].copy()
    except Exception as e:
        returnParameters = {}
    try:
        resource_id  = event.get('path','').split('/')[-1]
        if resource_id.isdigit():
            returnParameters['resource_id']  = resource_id
        else:
            return {"parsedParams": None, "err": 
                Exception("resource_id not a number")} 
    except Exception as e:
        return {"parsedParams": None, "err":e} # Generally bad idea to expose exceptions
    return {"parsedParams": returnParameters, "err":None}

def respond(err, errCode=400, res=None):
    return {
        'statusCode': str(errCode) if err else '200',
        'body': '{"message":' + json.dumps(err.message) + '}' if err else json.dumps(res,cls=DecimalEncoder),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
    
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def get_dynamodb_records(table_name, event):
    try:
        repo = DynamoRepository(table_name)
        validation_result = parse_parameters(event)
        
        resource_id = str(validation_result['parsedParams']["resource_id"])
        if validation_result['parsedParams'].get("startDate") is None:
            result = repo.query_by_partition_key(partition_key="EventId", partition_value=resource_id)
        else:
            start_date = int(validation_result['parsedParams']["startDate"])
            result = repo.query_by_partition_and_sort_key(partition_key="EventId", partition_value=resource_id,
                                                            sort_key="EventDay", sort_value=start_date)
        return respond(err=None, res=result)
        
    except Exception as e:
        print_exception(e)
        return respond(err=Exception('Not found'), errCode=404)
  
class DynamoRepository:

    def __init__(self, table_name):
        self.dynamo_client = resource(service_name='dynamodb', region_name='eu-west-1')   
        self.table_name = table_name 
        self.db_table = self.dynamo_client.Table(table_name)
    
    def query_by_partition_and_sort_key(self, partition_key, partition_value, sort_key, sort_value):
        response = self.db_table.query(KeyConditionExpression=
                                       Key(partition_key).eq(partition_value)
                                       & Key(sort_key).gte(sort_value))
                                   
        return response.get('Items')
    
    def query_by_partition_key(self, partition_key, partition_value):
        response = self.db_table.query(KeyConditionExpression=
                                       Key(partition_key).eq(partition_value))
                                   
        return response.get('Items')
    
    def update_dynamo_event_counter(self, event_name, event_datetime, event_count=1):
            self.dbTable.update_item(
            Key={
                'EventId': event_name, 
                'EventDay': event_datetime
            },
            ExpressionAttributeValues={":eventCount":event_count, ":ExpirationTime":self.expiration_time})   

def print_exception(e):
    print(''.join(['Exception ',str(type(e))]))             
    print(''.join(['Exception ',str(e.__doc__)]))
    print(''.join(['Exception ',str(e.message)]))
    
def lambda_handler(event, context):
    #table_name = 'poc-lambda-user-visits'
    table_name = 'poc-lambda-user-visits-sam'       
    return get_dynamodb_records(table_name, event)
