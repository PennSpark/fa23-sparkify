# Use the official AWS Lambda Python image as the base image
FROM public.ecr.aws/lambda/python:3.11
#FROM python:3.11 as build-image

# Set the working directory inside the container
#WORKDIR /var/task

# Copy the Lambda function code into the container
COPY lambda_function_ecr/ ${LAMBDA_TASK_ROOT}

# Install any additional dependencies (if needed)
# Example:
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

#resolves libGL.so.1 error
RUN yum update -y
RUN yum install libglvnd-glx -y
RUN yum install nano -y


# Define the handler function and runtime (modify accordingly)
CMD ["app.lambda_handler"]

