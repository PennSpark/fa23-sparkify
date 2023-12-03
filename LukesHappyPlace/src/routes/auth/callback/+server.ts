import { SPOTIFY_CLIENT_SECRET } from '$env/static/private';
import { PUBLIC_SPOTIFY_CLIENT_ID, PUBLIC_DOMAIN_NAME } from '$env/static/public';
import { error, redirect } from '@sveltejs/kit';

export async function GET({ url, cookies }) {
	const code = url.searchParams.get('code')!;
	/**
     * TODO: Uncomment this once working
    const state = url.searchParams.get('state')!;
    
    if(state != getState()) {
        throw error(400, {
            message: "Invalid State",
        });
    }
    */

	const response = await fetch('https://accounts.spotify.com/api/token', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
			Authorization: `Basic ${btoa(`${PUBLIC_SPOTIFY_CLIENT_ID}:${SPOTIFY_CLIENT_SECRET}`)}`
		},
		body: new URLSearchParams({
			grant_type: 'authorization_code',
			code: code,
			redirect_uri: `${PUBLIC_DOMAIN_NAME}/auth/callback`
		})
	});

	if (response.status === 200) {
		const body = await response.json();

		cookies.set('access_token', body.access_token, {
			httpOnly: true,
			secure: true,
			path: '/',
			sameSite: 'lax'
		});

		throw redirect(302, '/collage');
	} else {
		// Handle the error case here if needed
		await console.log(response.status + ' ' + response.statusText + ': ' + (await response.text()));
		throw error(500, {
			message: 'Internal Server Error'
		});
	}
}
