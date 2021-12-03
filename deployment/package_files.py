#!/usr/bin/python
'''
Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

Created on 3 Feb 2018
@author: Richard Freeman

This package is used rename and Zip the Lambda function.
'''

import os
import argparse
import zipfile

def package_file(inputpath, outputpath):
    
    current_path = get_curr_path()
    inputpath = os.path.join(current_path, inputpath)
    print(inputpath)
    outputpath = os.path.join(current_path, outputpath)
    print(outputpath)
    create_diectory_if_not_exist(outputpath)
    arcname = 'lambda_function.py'
    zipfile.ZipFile(outputpath, mode='w').write(inputpath, arcname)
    return outputpath
  
def get_curr_path():
    dir = os.path.dirname(__file__)
    schemafilename = os.path.abspath(os.path.dirname(dir))
    return schemafilename 
   
def create_diectory_if_not_exist(directory):
    if not os.path.exists(os.path.dirname(directory)):
        print('Creating dir: %s'%os.path.dirname(directory))
        os.makedirs(os.path.dirname(directory))     
            
def main():
    
    inputpath = 'lambda_dynamo_get/lambda_return_dynamo_records.py'   
    outputpath = 'package/lambda_return_dynamo_records.zip'
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputpath", type=str, required=False, help="The input file path")
    parser.add_argument("-o", "--outputpath", type=str, required=False, help="The output file path")
    args = parser.parse_args()
       
    if (args.inputpath is not None):
        inputpath = args.inputpath
    if (args.outputpath is not None):
        outputpath = args.outputpath
    package_file(inputpath, outputpath)
    

if __name__ == '__main__':
    main()