import { PUBLIC_SPOTIFY_CLIENT_ID, PUBLIC_DOMAIN_NAME } from '$env/static/public';
import getState from '$lib/state';
import { redirect } from '@sveltejs/kit';

// https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player

export async function GET({ cookies }) {
	const scope = 'user-read-private user-read-email user-top-read';
	const state = getState();

	const params = new URLSearchParams({
		response_type: 'code',
		client_id: PUBLIC_SPOTIFY_CLIENT_ID,
		scope: scope,
		redirect_uri: `${PUBLIC_DOMAIN_NAME}/auth/callback`,
		state: state
	});

	if(cookies.get("access_token") != undefined) {
		throw redirect(302, '/collage');
	} else {
		throw redirect(302, 'https://accounts.spotify.com/authorize/?' + params.toString());
	}
}
