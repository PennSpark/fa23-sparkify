

import AWS from 'aws-sdk';
import type { AWSError } from 'aws-sdk'
import type { InvocationResponse } from 'aws-sdk/clients/lambda';
const BUCKET_NAME = 'fa23-sparkify-bucket';


AWS.config.update({
    accessKeyId: 'AKIA4FGSHVMSEXPOF6VA',
    secretAccessKey: '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',
    region: 'us-east-1',
});



export async function callLambda(urlList : string[]) { 
    //urlList is string[] of urls but i couldn't figure out how to fix a type bug
    //so put it as any
    try {
        const lambda = new AWS.Lambda();

        const params = {
        FunctionName: 'sam-app-HelloWorldFunction-Kr2SNYoWtrgR',
        Payload: JSON.stringify({ urls: urlList }), // Your payload
        };

        lambda.invoke(params, function (err : AWSError, data : InvocationResponse) {
        if (err) {
            console.error('Error calling Lambda:', err);
        } else {
            //TODO: Save lambda output to svelte state
            console.log('Lambda Response:', data);
        }
        });

    } catch (error) {
    console.error('Error calling Lambda:', error);
}
}


export async function callS3(key : string) { 
    //key is a string holding the name of the album cover stored in S3
    const s3 = new AWS.S3();
    //console.log(req.body);
    const params = {
        Bucket: BUCKET_NAME,
        Key: key,
        Expires: 3600 
    };

    s3.getSignedUrl('getObject', params, (err : Error, url : string) => {
        if (err) {
            console.error(err);
        } else {
            //TODO: Save signedS3Url to svelte state
            console.log(url);
        }
    });
}

