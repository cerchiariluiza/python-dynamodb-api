'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 28 Jan 2018

pip install locust

@author: Richard Freeman
'''
from locust import HttpLocust, TaskSet, task

class SimpleLocustTest(TaskSet):

    @task
    def get_something(self):
        self.client.get("/prod/visits/324?startDate=20171014")

class LocustTests(HttpLocust):
    task_set = SimpleLocustTest