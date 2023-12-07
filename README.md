# fa23-sparkify
our happy place

## Deployment Steps

Used the following AWS link as reference: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions

We used an AWS Lambda function to run our AI models, and put the outputs of the AI models (segmented images) into our S3 bucket, from where we would output signed URLs that could be displayed on the frontend. 

Steps Taken to Deploy Lambda Function:
1. Dockerized code that was written for an AWS Lambda function using a Dockerfile, including packages in requirements.txt file
  - Environment variables such as credentials should be set up in the Dockerfile, not referenced directly in the code
2. Tested the code locally, and resolved errors using curL command shown in the AWS link above (if you want to test the capability of a Dockerized Lambda function, you MUST use that command)
3. Uploaded the container to a private AWS Elastic Container Repository(ECR) using instructions in the AWS link
4. Created an AWS Lambda function via AWS console, selecting the option to generate a lambda function via a Docker container
5. Tested Lambda function using Test Events via AWS console
6. Tested from deployed webapp

Note: had to download AI models locally and include them in the Dockerfile. This does 2 things. One, it makes our cold start case faster because we don't have to download the model from the Internet. Two, AWS Lambda generates a read-only environment, unless you create a /tmp folder that can be written to (but we didn't think it was worth the time to figure out how to get the Lambda function to write the AI models to a /tmp folder and do all that when we could just include it in the container)

Steps Taken to Set Up S3 Bucket:
1. Create S3 Bucket via console
2. Disallow all public access to the S3 Bucket
3. Allow IAM User assigned for the Lambda function to perform necessary actions to the S3 Bucket via policy statement

Steps Taken to Set Up IAM Permissions:
1. Create IAM user for Lambda function and give it permissions so that it can access S3, and perform all necessary Lambda function actions
