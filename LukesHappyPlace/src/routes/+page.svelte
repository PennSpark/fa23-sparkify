<script lang="ts">
	import type { Artist, Track } from "../lib/types";

    export let data: { tracks: Track[], artists: Artist[] };
</script>

{#if data.tracks.length === 0 && data.artists.length === 0}
    <a href="/auth/login">LOGIN</a>
{:else}
    <h1>Top Tracks</h1>
    {#each data.tracks as track}
        <p>{track.name}</p>
    {/each}

    <h1>Top Artists</h1>
    {#each data.artists as artist}
        <p>{artist.name}</p>
    {/each}
{/if}
