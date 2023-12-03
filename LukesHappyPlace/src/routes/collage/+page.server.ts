import { callLambda, callS3 } from "$lib/awsCalls";

export async function load({ cookies, fetch }) {
    const access_token = cookies.get("access_token");
    // TODO: deal with login + handle access_token expired
    
    if(!access_token) return { tracks: [], artists: [] };

    // fetch top artists/tracks
    const response = await fetch("/api/spotify");
    const { tracks } = await response.json();

    const urls: string[] = tracks.map((track: any) => track.album.img);
    
    // send to S3 for processing
    await callLambda(urls);

    // call S3 to retrieve processed images
    const images = [];
    for(const url in urls) {
        const arr = url.split("/");
        images.push(await callS3(arr[arr.length - 1]));
    }

    // return image urls
    return {
        images: images,
    }
}
