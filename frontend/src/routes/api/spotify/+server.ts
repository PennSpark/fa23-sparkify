import { error, json } from '@sveltejs/kit';
import type { Track } from '$lib/types';
import { getTrackFromObject } from '$lib/utils';

export async function GET({ cookies }) {
	const limit = 50;

	let expired = false;
	const access_token = cookies.get('access_token')!;

	if (!access_token) error(500, 'No access token provided');

	const tracks = await getTopTracks(limit, access_token);

	if (tracks.length === 0) {
		expired = true;
	}

	return json({
		expired: expired,
		tracks: tracks
	});
}

async function getTopTracks(limit: number, access_token: string): Promise<Track[]> {
	/**
	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
	 */
	const ENDPOINT = 'https://api.spotify.com/v1/me/top/tracks';
	const tracks: Track[] = [];

	const response = await getItem(ENDPOINT, access_token, limit);
	if (response.error) {
		if (response.error.message === 'The access token expired') {
			return tracks;
		}
		error(500, response.error.message);
	}

	const len = Math.min(limit, response.total);
	for (let i = 0; i < len; ++i) {
		tracks.push(getTrackFromObject(response.items[i]));
	}

	return tracks;
}

// async function getTopArtists(count: number, access_token: string): Promise<Artist[]> {
// 	/**
// 	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
// 	 */
// 	const ENDPOINT = 'https://api.spotify.com/v1/me/top/artists';
// 	const artists: Artist[] = [];

// 	const response = await getItem(ENDPOINT, access_token);
// 	if (response.error) {
// 		if (response.error.message === 'The access token expired') {
// 			return artists;
// 		}
// 		throw error(500, response.error.message);
// 	}

// 	const len = Math.min(count, response.total);
// 	for (let i = 0; i < len; ++i) {
// 		artists.push(getArtistFromObject(response.items[i]));
// 	}

// 	return artists;
// }

async function getItem(endpoint: string, access_token: string, limit: number) {
	endpoint += "?limit=" + limit;
	const response = await fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	});

	/**
	 * https://developer.spotify.com/documentation/web-api/concepts/api-calls
	 */
	// if(response.status > 300) {
	// 	await console.log(response.status + " " + response.statusText + ": " + await response.text());
	// }

	return response.json();
}
