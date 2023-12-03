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
    const processed: { images: string[] } = await callLambda(urls);
    console.log(processed)

    // call S3 to retrieve processed images
    const images = [];
    for(const processed_img in processed.images) {
        images.push(await callS3(processed_img));
    }

    // test
    images.push(await callS3("ab67616d0000b273cdb645498cd3d8a2db4d05e1.png"));

    // return image urls
    return {
        images: images,
    }
}
