import { error, json } from "@sveltejs/kit";
import { getTopArtists, getTopTracks } from "$lib/queries";

export async function GET({ cookies }) {
	const access_token = cookies.get("access_token")!;

	if(!access_token) throw error(500, "No access token provided");

	return json({
		tracks: await getTopTracks(5, access_token),
		artists: await getTopArtists(5, access_token)
	});
}
