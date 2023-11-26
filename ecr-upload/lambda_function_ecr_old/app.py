import json
import requests
from collage import process_collage_images

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

    """return {
        "statusCode": 200,
        "body": json.dumps({
            "event": event
            # "location": ip.text.replace("\n", "")
        }),
    }"""

    try:
        #https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        event = event
        body = event['body']
        url_list = body.get('urls', [])
        process_collage_images(url_list, local=False)
        
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)

        raise e




    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "IT WORKED",
            # "location": ip.text.replace("\n", "")
        }),
    }
