set template=lambda-dynamo-data-api
set region=<your-region>
aws cloudformation delete-stack --stack-name %template% --region %region%

