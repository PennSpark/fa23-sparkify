import { error, json } from "@sveltejs/kit";
import type { Artist, Track } from "$lib/types";
import { getArtistFromObject, getTrackFromObject } from "$lib/utils";

export async function GET({ cookies }) {
	let expired = false;
	const access_token = cookies.get("access_token")!;

	if(!access_token) throw error(500, "No access token provided");

	const tracks = await getTopTracks(5, access_token);
	const artists = await getTopArtists(5, access_token);

	if(tracks.length === 0 || artists.length === 0) {
		expired = true;
	}
	
	return json({
		expired: expired,
		tracks: tracks,
		artists: artists,
	});
}


async function getTopTracks(count: number, access_token: string): Promise<Track[]>  {
	/**
	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
	 */
	const ENDPOINT = "https://api.spotify.com/v1/me/top/tracks";
	const tracks: Track[] = [];

	const response = await getItem(ENDPOINT, access_token);
	if(response.error) {
		if(response.error.message === "The access token expired") {
			return tracks;
		}
		throw error(500, response.error.message);
	}

	const len = Math.min(count, response.total);
	for(let i = 0; i < len; ++i) {
		tracks.push(getTrackFromObject(response.items[i]));
	}

	return tracks;
}

async function getTopArtists(count: number, access_token: string): Promise<Artist[]>  {
	/**
	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
	 */
	const ENDPOINT = "https://api.spotify.com/v1/me/top/artists";
	const artists: Artist[] = [];

	const response = await getItem(ENDPOINT, access_token);
	if(response.error) {
		if(response.error.message === "The access token expired") {
			return artists;
		}
		throw error(500, response.error.message);
	}

	const len = Math.min(count, response.total);
	for(let i = 0; i < len; ++i) {
		artists.push(getArtistFromObject(response.items[i]));
	}

	return artists;
}

async function getItem(endpoint: string, access_token: string) {
	const response = await fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${access_token}`,
		},
	});

	/**
	 * https://developer.spotify.com/documentation/web-api/concepts/api-calls
	 */
	// if(response.status > 300) {
	// 	await console.log(response.status + " " + response.statusText + ": " + await response.text());
	// }

	return response.json();
}
