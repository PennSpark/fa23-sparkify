import { getAccessToken  } from "./api";

export type Track = {
	name: string;
	artists: string[];
	url: string;
	album: Album;
}

export type Album = {
	name: string;
	artists: string[]
	url: string;
	img: string;
	// tracks: Track[] // might not be necessary
}

export async function getTopTracks(count: number): Promise<Track[]>  {
	/**
	 * https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
	 */
	const ENDPOINT = "https://api.spotify.com/v1/me/top/tracks";
	const tracks: Track[] = [];

	const response = await getItem(ENDPOINT);

	let len = Math.min(count, response.total);
	for(let i = 0; i < len; ++i) {
		tracks.push(getTrackFromObject(response.items[i]));
	}

	return tracks;
}

/** HELPERS */

async function getItem(endpoint: string) {
	const { access_token } = await getAccessToken();

	const response = await fetch(endpoint, {
		headers: {
			Authorization: `Bearer ${access_token}`,
		},
	});

	/**
	 * https://developer.spotify.com/documentation/web-api/concepts/api-calls
	 */
	if(response.status > 300) {
		await console.log(await response.statusText);
	}

	return response.json();
}

function getTrackFromObject(trackObject: any): Track {
	return {
		name: trackObject.name,
		artists: trackObject.artists.map((artist: { name: string }) => artist.name),
		url: trackObject.external_urls.spotify,
		album: getAlbumFromObject(trackObject.album),
	}
}

function getAlbumFromObject(albumObject: any): Album {
	return {
		name: albumObject.name,
		artists: albumObject.artists.map((artist: { name: string }) => artist.name),
		url: albumObject.external_urls.spotify,
		img: albumObject.images[0].url,
	}
}
