import {
    PUBLIC_SPOTIFY_CLIENT_ID,
    PUBLIC_DOMAIN_NAME,
} from "$env/static/public";
import { generateRandomString } from "$lib/utils";
import { redirect } from "@sveltejs/kit";

// https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player

export function load() {
    const scope = "user-read-private user-read-email user-top-read";
    const state = generateRandomString(16);
    const params = new URLSearchParams({
        response_type: "code",
        client_id: PUBLIC_SPOTIFY_CLIENT_ID,
        scope: scope,
        redirect_uri: `${PUBLIC_DOMAIN_NAME}/auth/callback`,
        state: state
    });
    
    throw redirect(302, "https://accounts.spotify.com/authorize/?" + params.toString());
}
