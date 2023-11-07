import { SPOTIFY_CLIENT_SECRET } from "$env/static/private";
import {
    PUBLIC_SPOTIFY_CLIENT_ID,
    PUBLIC_DOMAIN_NAME,
} from "$env/static/public";
import { error, redirect } from "@sveltejs/kit";

export async function GET({ url, cookies }) {
    const code = url.searchParams.get('code')!;

    const response = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': `Basic ${btoa(`${PUBLIC_SPOTIFY_CLIENT_ID}:${SPOTIFY_CLIENT_SECRET}`)}`
        },
        body: new URLSearchParams({
            code: code,
            redirect_uri: `${PUBLIC_DOMAIN_NAME}/auth/callback`,
            grant_type: 'authorization_code'
        }),
    });

    if(response.status === 200) {
        const body = await response.json();

        cookies.set("access_token", body.access_token, {
            httpOnly: true,
            secure: true,
             path: '/',
             sameSite: 'lax',
        });

        throw redirect(302, "/");
    }
    else {
        // Handle the error case here if needed
        throw error(500, {
            message: "Internal Server Error",
        });
    }
}
