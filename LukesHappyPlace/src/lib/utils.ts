import type { Track, Album, Artist } from "./types";

export function generateRandomString(length: number): string {
	let text = '';
	const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  
	for (let i = 0; i < length; i++) {
	  text += possible.charAt(Math.floor(Math.random() * possible.length));
	}
	return text;
  };

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getTrackFromObject(trackObject: any): Track {
	return {
		name: trackObject.name,
		artists: trackObject.artists.map((artist: { name: string }) => artist.name),
		url: trackObject.external_urls.spotify,
		album: getAlbumFromObject(trackObject.album),
	}
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getAlbumFromObject(albumObject: any): Album {
	return {
		name: albumObject.name,
		artists: albumObject.artists.map((artist: { name: string }) => artist.name),
		url: albumObject.external_urls.spotify,
		img: albumObject.images[0].url,
	}
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getArtistFromObject(artistObject: any): Artist {
    return {
        name: artistObject.name,
        genres: artistObject.genres,
        url: artistObject.external_urls.spotify,
        imgs: artistObject.images.map((img: { url: string }) => img.url),
    }
}
