import { AWS_ACCESS_KEY_ID, AWS_LAMBDA_PASSWORD, AWS_SECRET_ACCESS_KEY } from '$env/static/private';
import AWS from 'aws-sdk';
import type { AWSError } from 'aws-sdk';
import type { InvocationResponse } from 'aws-sdk/clients/lambda';
const BUCKET_NAME = 'fa23-sparkify-bucket';

AWS.config.update({
	accessKeyId: AWS_ACCESS_KEY_ID,
	secretAccessKey: AWS_SECRET_ACCESS_KEY,
	region: 'us-east-1'
});

export async function callLambda(urlList: string[]) {
	try {
		const lambda = new AWS.Lambda();

		const params = {
			FunctionName: 'finalLambda',
			Payload: JSON.stringify({
				body: {
					passcode: AWS_LAMBDA_PASSWORD,
					urls: urlList
				}
			})
		};

		return new Promise((resolve, reject) => {
			lambda.invoke(params, function (err: AWSError, data: InvocationResponse) {
				if (err) {
					reject(err);
				} else {
					resolve(data);
				}
			});
		});
	} catch (error) {
		console.error('Error calling Lambda:', error);
	}
}

export async function callS3(key: string) {
	//key is a string holding the name of the album cover stored in S3
	const s3 = new AWS.S3();
	//console.log(req.body);
	const params = {
		Bucket: BUCKET_NAME,
		Key: key,
		Expires: 3600
	};

	// make it call getSignedUrls so it doesn't have to reconnect every fetch
	return new Promise((resolve, reject) => {
		s3.getSignedUrl('getObject', params, (err: Error, url: string) => {
			if (err) {
				reject(err);
			} else {
				resolve(url);
			}
		});
	});
}
