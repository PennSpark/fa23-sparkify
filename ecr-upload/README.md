11/25/2023

what was done today:
- downgraded pytorch and torchvision so that segfault didn't happen
- decided that we are going to put a password/auth phrase on our public repo
  so not everyone can just call it easily we are going to use a os.getenv() kind of call
  so that you can't just go inside our code and see what it is how it works is that env variables
  stored in containers are separate from the images so people wn't be able to see our special passphrase
- decided that we are going to go with the original option of doing s3 directly from container so use lambda_function_ecr_old
- pytorch_2.0.1 is the name of the docker image with the most recent updates (but does not have the original option)

todo:
- add auth phrase as environment variable
- YOU NEED TO BE WORKING ON THE lambda_function_ecr_old code because that contains the code that does s3 directly from container
- change code to be the one that does s3 directly from the container (also using environment variables for secret keys)

documentation to look at:
https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions

commands:
before building docker or anything, you must run: aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/y4w7m0j8

this is because you are using an aws hosted python image so you have to authenticate as an aws user

to build:
docker build -t <name of image> .

to run on 9090:8080:
docker run -p 9000:8080 <name of image>

to test lambda function:
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"body": {"urls":["https://i.scdn.co/image/ab67616d00001e02fb1808a11a086d2ba6edff51", "https://i.scdn.co/image/ab6761610000e5eb95cc5cc99f557587636f7f29"]}}'

