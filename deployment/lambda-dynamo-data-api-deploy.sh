#!/usr/bin/env bash

#Variables
template=lambda-dynamo-data-api
python_file=lambda_return_dynamo_records.py
bucket=<your-bucket>
region=<your-region>

#Create Zip file of your Lambda code (works on Windows and Linux) 
python ../deployment/package_files.py -i lambda_dynamo_get/$python_file -o package/$template.zip

#Package your Serverless Stack using SAM + Cloudformation
aws cloudformation package --template-file ../deployment/$template.yaml --output-template-file ../package/$template-output.yaml --s3-bucket $bucket --s3-prefix backend --region $region

#Deploy your Serverless Stack using SAM + Cloudformation
aws cloudformation deploy --template-file ../package/$template-output.yaml --stack-name $template --capabilities CAPABILITY_IAM --region $region