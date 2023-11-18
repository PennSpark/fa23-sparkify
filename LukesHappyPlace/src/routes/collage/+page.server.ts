import { redirect } from "@sveltejs/kit";

export async function load({ cookies, fetch }) {
    const access_token = cookies.get("access_token");
    // TODO: deal with login + handle access_token expired
    
    if(!access_token) return { tracks: [], artists: [] };

    const response = await fetch("/api/spotify");
    const data = await response.json();

    if(data.expired) throw redirect(302, "/auth/login");

    return await data;
}
