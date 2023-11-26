import json
import requests

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    """]
    Receives:

    POST /your-lambda-endpoint
    Content-Type: application/json

    urls is stored in body
    {
    "urls": [
        "https://example.com/path/to/image1.jpg",
        "https://example.com/path/to/image2.jpg",
        "https://example.com/path/to/image3.jpg"
    ]
    }


    """

    try:
        #https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        ecr_event = {'body': {'urls':["https://i.scdn.co/image/ab67616d00001e02fb1808a11a086d2ba6edff51"]}}
        resp = requests.post("http://localhost:9000/2015-03-31/functions/function/invocations", data=json.dumps(ecr_event))
        print(resp)
        print(resp.text)
        print("finished post request")
        
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)

        raise e




    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }


#test ecr lambda by using curl lambda invoke commands