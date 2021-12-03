'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 13 Jan 2018

@author: rfreeman

Lambda DynamoDB unit tests and mocking

pip install mock

'''

import mock
import unittest
import json
from lambda_dynamo_get import lambda_return_dynamo_records as lambda_query_dynamo

TEST_TABLE_NAME ='poc-lambda-user-visits'

class TestIndexGetMethod(unittest.TestCase):
    def setUp(self):
        self.testJsonData = json.loads("{\"queryStringParameters\": {\"startDate\": \"20171013\"}," \
                            "\"httpMethod\": \"GET\",\"path\": \"/path/to/resource/324\",\"headers\": " \
                            "null} ")
        
        self.testInvalidJsonData = "{ invalid JSON request!} "
        
        self.testNoUserJsonData = json.loads("{\"queryStringParameters\": {\"startDate\": \"20171013\"}," \
                            "\"httpMethod\": \"GET\",\"path\": \"/path/to/resource/899873244\",\"headers\": " \
                            "null} ")
        
    def tearDown(self):        
        pass
    
    def test_validparameters_parseparameters_pass(self):
        parameters = lambda_query_dynamo.parse_parameters(self.testJsonData)
        assert parameters['parsedParams']['startDate'] == u'20171013'
        assert parameters['parsedParams']['resource_id'] == u'324'
        
    def test_invalidjson_getrecord_notfound404(self):
        result = lambda_query_dynamo.get_dynamodb_records(TEST_TABLE_NAME, self.testInvalidJsonData)
        assert result['statusCode'] == '404'
        assert json.loads(result['body'])['message'] == "Not found"
        
    @mock.patch.object(lambda_query_dynamo.DynamoRepository,
                       "query_by_partition_and_sort_key",
                       return_value=['item'])
    def test_validid_checkstatus_status200(self, mock_query_by_partition_and_sort_key):
        result = lambda_query_dynamo.get_dynamodb_records(TEST_TABLE_NAME, 
                                                         self.testJsonData)
        assert result['statusCode'] == '200' 
            
    @mock.patch.object(lambda_query_dynamo.DynamoRepository,
                       "query_by_partition_and_sort_key",
                       return_value=['item'])
    def test_validid_getrecord_validparam(self, mock_query_by_partition_and_sort_key):
        lambda_query_dynamo.get_dynamodb_records(TEST_TABLE_NAME, self.testJsonData)
        mock_query_by_partition_and_sort_key.assert_called_with(partition_key='EventId',
                                                            partition_value=u'324',
                                                            sort_key='EventDay',
                                                            sort_value=20171013)
    
        


    