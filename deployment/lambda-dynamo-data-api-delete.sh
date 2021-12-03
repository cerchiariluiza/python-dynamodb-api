#!/usr/bin/env bash
template=lambda-dynamo-data-api
region=<your-region>
aws cloudformation delete-stack --stack-name $template --region $region
