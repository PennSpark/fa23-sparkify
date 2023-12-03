import { callLambda, callS3 } from '$lib/awsCalls';
import type { Image } from '$lib/types';

export async function load({ cookies, fetch }) {
	const access_token = cookies.get('access_token');
	// TODO: deal with login + handle access_token expired

	if (!access_token) return { tracks: [], artists: [] };

	// fetch top artists/tracks
	const response = await fetch('/api/spotify');
	const { tracks } = await response.json();

	const urls: string[] = tracks.map((track: { album: { img: string } }) => track.album.img);

	// send to S3 for processing
	const { Payload } = await callLambda(urls);
	const result = await JSON.parse(JSON.parse(Buffer.from(Payload).toString()).body); // bruh

	// call S3 to retrieve images
	const cropped_images: Image[] = [];
	for (let i = 0; i < result.urlsPutIntoS3.cropped_image_data.length; i++) {
		cropped_images.push({
			url: await callS3(result.urlsPutIntoS3.cropped_image_data[i].url.substr(1)),
			rank: result.urlsPutIntoS3.cropped_image_data[i].rank
		});
	}
	const uncropped_images: Image[] = [];
	for (let i = 0; i < result.urlsPutIntoS3.uncropped_image_data.length; i++) {
		uncropped_images.push({
			url: result.urlsPutIntoS3.uncropped_image_data[i].url,
			rank: result.urlsPutIntoS3.uncropped_image_data[i].rank
		});
	}
	// descending order
	cropped_images.sort((a, b) => {
		return a.rank - b.rank;
	});
	uncropped_images.sort((a, b) => {
		return a.rank - b.rank;
	});

	// return image urls
	return {
		cropped_images: cropped_images,
		uncropped_images: uncropped_images,
		palette: result.urlsPutIntoS3.dominant_color
	};
}
