import { callS3 } from "$lib/awsCalls";
import { redirect } from "@sveltejs/kit";

export async function load({ cookies, fetch }) {
    const access_token = cookies.get("access_token");
    // TODO: deal with login + handle access_token expired
    
    if(!access_token) return { tracks: [], artists: [] };

    // fetch top artists/tracks
    const response = await fetch("/api/spotify");
    
    // send to S3 for processing

    // call S3 to retrieve processed images
    // test
    const urls = [];
    urls.push(await callS3("ab67616d00001e02fb1808a11a086d2ba6edff51.png"));

    // return image urls
    return {
        urls: urls,
    }

    const data = await response.json();

    if(data.expired) throw redirect(302, "/auth/login");
    return await data;
}
