Copyright (c) 2017-2018 RFWOLF Ltd and Richard Freeman. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). 
You may not use this file except in compliance with the License. 
A copy of the License is located at  
    http://www.apache.org/licenses/LICENSE-2.0
or in the "license" file accompanying this file. This file is distributed 
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
express or implied. See the License for the specific language governing 
permissions and limitations under the License.

This repository demonstrated API Gateway, Lambda and DynamoDB can be used together to create a Serverless Microservice data API.
More details and updates are available on [www.rfwolf.com](http://www.rfwolf.com/)

# Building a Scalable Serverless REST Data API

The repository includes:
* Code to create, insert data and query a DynamoDB table. 
* A simple parameter parsing Lambda function and a more complex one that can query DynamoDB. 
* Launch and debug a Lambda locally
* Unit testing and mocking
* Performance testing
* Creating the AWS Resources
* Building, deploying you serverless stack
* Deleting your serverless stack
* Single Stack Deployment or Deletion Scripts

# Quick Start
-----------
Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/installing.html):

On LINUX
```
$ pip install awscli
```

For Windows Download the [MSI Installer](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#install-msi-on-windows)

Setup the credentials `~/.aws/credentials` manually or by running `$ aws configure`

```code-block:: ini
    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET
```
Next, install the dependent libraries

```code-block:: sh
$ pip install -r requirements.txt
```

# Testing

## Unit testing
Run all the unit tests
```
$ python -m unittest discover
```

## Integration testing
Run an integration test using the AWS CLI
```
$ aws lambda invoke --invocation-type Event --function-name  --region <your-region> --payload file://sample_data/request-api-gateway-valid-date.txt outputfile.tmp
```

## Performance / load testing
Launch locust and access web UI
```
$ locust -f locust_test_script.py --host=https://XXXXXXXXXX.execute-api.<your-region>.amazonaws.com

```
For the Web UI, visit: http://localhost:8089/

# Build and Deploy your Serverless Stack
The following demonstrates the creation of your complete Serverless Microservice Stack.
* AWS CLI - Bucket, and IAM Policies and Roles
* SAM - API Gateway, Lambda and DynamoDB can be used together to create a Serverless Microservice data API.


## Creating base Serverless Resources
-----------

### Creating your S3 Bucket
The Bucket and Roles are deliberately not included as part of the of SAM YAML template, as I found that they will often be reused by other services so will probably outlive the CloudFormation Stack.

```
#Windows:
set bucket=<your-bucket>
set region=<your-region>
aws s3api create-bucket --bucket %bucket% --region <your-region> --create-bucket-configuration LocationConstraint=<your-region>

#LINUX
$ bucket=<your-bucket>
$ region=<your-region>
$ aws s3api create-bucket --bucket $bucket --region <your-region> --create-bucket-configuration LocationConstraint=<your-region>
```

### Creating you IAM Policies and Roles

```
#Windows and LINUX:
$ aws iam create-policy --policy-name lambda-cloud-write-cli --policy-document  file://IAM/lambda-cloud-write.json

#replace <aws-account-id> in JSON iam/dynamo-readonly-counters.json file with your account ID (see IAM)
$ aws iam create-policy --policy-name dynamo-readonly-counters-cli --policy-document  file://IAM/dynamo-readonly-counters.json

$ aws iam create-role --role-name lambda-dynamo-data-api-cli --assume-role-policy-document file://IAM/role-lambda-trust.json --description "Allows Lambda functions to call AWS services on your behalf."

#replace <aws-account-id> with your account ID (see IAM)
$ aws iam attach-role-policy --policy-arn arn:aws:iam::<aws-account-id>:policy/lambda-cloud-write-cli --role-name lambda-dynamo-data-api-cli
```

## Using SAM to Package and deploy your Serverless Stack

### Windows
```
set template=lambda-dynamo-data-api
set python_file=lambda_return_dynamo_records.py
set bucket=<your-bucket>
set region=<your-region>

#Create Zip file of your Lambda code (works on Windows and Linux) 
python deployment\package_files.py -i lambda_dynamo_get\%python_file% -o package\%template%.zip

#Package your Serverless Stack using SAM + Cloudformation
aws cloudformation package --template-file deployment\%template%.yaml --output-template-file package\%template%-output.yaml --s3-bucket %bucket% --s3-prefix backend --region %region%

#Deploy your Serverless Stack using SAM + Cloudformation
aws cloudformation deploy --template-file package\%template%-output.yaml --stack-name %template%  --capabilities CAPABILITY_IAM --region %region%

#Delete your Stack
aws cloudformation delete-stack --stack-name %template% --region %region%
```

### Linux
```
#Make sure you are on the latest pip and AWS CLI
$ aws --v
$ sudo apt-get install python3-pip
$ pip3 install awscli --upgrade

#Variables
$ template=lambda-dynamo-data-api
$ python_file=lambda_return_dynamo_records.py
$ bucket=<your-bucket>
$ region=<your-region>

#Create Zip file of your Lambda code (works on Windows and Linux) 
$ python deployment/package_files.py -i lambda_dynamo_get/$python_file -o package/$template.zip

#Package your Serverless Stack using SAM + Cloudformation
$ aws cloudformation package --template-file deployment/$template.yaml --output-template-file package/$template-output.yaml --s3-bucket $bucket --s3-prefix backend --region $region

#Deploy your Serverless Stack using SAM + Cloudformation
$ aws cloudformation deploy --template-file package/$template-output.yaml --stack-name $template --capabilities CAPABILITY_IAM --region $region

#Delete your Stack
$ aws cloudformation delete-stack --stack-name $template --region $region
```

### Single Stack Deployment or Deletion Scripts
 
The above Python Build, package and deploy are also available under the deployment folder as a single Windows batch `lambda-dynamo-data-api-deploy.bat` and LINUX Shell as `./lambda-dynamo-data-api-deploy.sh` as single file you can change for your environment. For LINUX make sure you set `chmod +x deployment/lambda-dynamo-data-api-deploy.sh` before executing.

Once you no longer need the Serverless stack you can delete it using `lambda-dynamo-data-api-delete.bat` for Windows or `./lambda-dynamo-data-api-delete.sh` for LINUX.
