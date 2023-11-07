import type { Artist, Track } from "./types";
import { getArtistFromObject, getTrackFromObject } from "./utils";

export async function getTopTracks(count: number, access_token: string): Promise<Track[]>  {
	/**
	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
	 */
	const ENDPOINT = "https://api.spotify.com/v1/me/top/tracks";
	const tracks: Track[] = [];

	const response = await getItem(ENDPOINT, access_token);

	const len = Math.min(count, response.total);
	for(let i = 0; i < len; ++i) {
		tracks.push(getTrackFromObject(response.items[i]));
	}

	return tracks;
}

export async function getTopArtists(count: number, access_token: string): Promise<Artist[]>  {
	/**
	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
	 */
	const ENDPOINT = "https://api.spotify.com/v1/me/top/artists";
	const artists: Artist[] = [];

	const response = await getItem(ENDPOINT, access_token);

	const len = Math.min(count, response.total);
	for(let i = 0; i < len; ++i) {
		artists.push(getArtistFromObject(response.items[i]));
	}

	return artists;
}

/** HELPERS */
async function getItem(endpoint: string, access_token: string) {
	const response = await fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${access_token}`,
		},
	});

	/**
	 * https://developer.spotify.com/documentation/web-api/concepts/api-calls
	 */
	if(response.status > 300) {
		await console.log(response.statusText);
	}

	return response.json();
}
