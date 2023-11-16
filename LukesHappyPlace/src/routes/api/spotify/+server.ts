import { error, json, redirect } from "@sveltejs/kit";
import { getTopArtists, getTopTracks } from "$lib/queries";

export async function GET({ cookies }) {
	const access_token = cookies.get("access_token")!;

	if(!access_token) throw error(500, "No access token provided");

	const tracks = await getTopTracks(5, access_token);
	if(tracks.length === 0) throw redirect(302, "/auth/login");

	const artists = await getTopArtists(5, access_token);
	if(artists.length === 0) throw redirect(302, "/auth/login");

	return json({
		tracks: tracks,
		artists: artists,
	});
}
