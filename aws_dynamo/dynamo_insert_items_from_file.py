'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 20 Jan 2018

@author: Richard Freeman

This packages inserts records from a file into DynamoDB

'''
from __future__ import print_function
from boto3 import resource
import csv

class DynamoRepository:
    def __init__(self, target_dynamo_table, region='eu-west-1'):
        self.dynamodb = resource(service_name='dynamodb', region_name=region)
        self.target_dynamo_table = target_dynamo_table
        self.table = self.dynamodb.Table(self.target_dynamo_table)
        
    def update_dynamo_event_counter(self, event_name, event_datetime, event_count=1):
        response = self.table.update_item(
                Key={
            'EventId': str(event_name), 
            'EventDay': int(event_datetime)
        },
        ExpressionAttributeValues={":eventCount":int(event_count)},
        UpdateExpression="ADD EventCount :eventCount")
        return response
                     
def main():
    #uncomment for manual setup
    #table_name = 'poc-lambda-user-visits'
     
    #uncomment for SAM deployment
    table_name = 'poc-lambda-user-visits-sam' 
    input_data_path = '../sample_data/dynamodb-sample-data.txt'
     
    dynamoRepo = DynamoRepository(table_name)
    with open(input_data_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            response = dynamoRepo.update_dynamo_event_counter(row['EventId'], 
                                                   row['EventDay'], 
                                                   row['EventCount'])
            print(response)
    
    
if __name__ == '__main__':
    main()