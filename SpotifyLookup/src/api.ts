import dotenv from "dotenv";
dotenv.config();

const SPOTIFY_CLIENT_ID = process.env.SPOTIFY_CLIENT_ID!;
const SPOTIFY_CLIENT_SECRET = process.env.SPOTIFY_CLIENT_SECRET!;
const SPOTIFY_REFRESH_TOKEN = process.env.SPOTIFY_REFRESH_TOKEN!;

export async function getAccessToken() {
	/**
	 * Uses a refresh token (currently you have to manually get that) 
	 * and recieves a valid access token that expires in i think an hour
	 */
	const params = new URLSearchParams();
	params.append("grant_type", "refresh_token");
	params.append("refresh_token", SPOTIFY_REFRESH_TOKEN);

	const response = await fetch("https://accounts.spotify.com/api/token", {
		method: "POST",
		headers: {
			Authorization: `Basic ${btoa(`${SPOTIFY_CLIENT_ID}:${SPOTIFY_CLIENT_SECRET}`)}`,
			"Content-Type": "application/x-www-form-urlencoded",
		},
		body: params,
	});

	return response.json();
}
