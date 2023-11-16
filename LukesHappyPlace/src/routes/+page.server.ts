export async function load({ cookies, fetch }) {
    const access_token = cookies.get("access_token");
    
    if(!access_token) return { tracks: [], artists: [] };

    const response = await fetch("/api/spotify");
    const data = await response.json();

    return await data;
}
