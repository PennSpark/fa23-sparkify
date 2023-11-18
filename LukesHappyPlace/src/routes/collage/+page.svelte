<script lang="ts">
	import { onMount } from "svelte";
    import output from "./output.json";
	import Button from "$lib/components/Button.svelte";
	import type { Artist, Track } from "$lib/types";

    export let data: { expired: boolean, tracks: Track[], artists: Artist[] };
    
    let bgstyle = 
        `
            position: absolute;
            width: 400px;
            height: 400px;
            overflow: hidden;
            background-color: rgb(
                ${output.dominant_color[0]} 
                ${output.dominant_color[1]} 
                ${output.dominant_color[2]}
            );
        `;

    const cropped_imgs = output.cropped_image_data.sort((a,b) => {
        return a.rank - b.rank;
    });
</script>

<p>
    COLLAGE!!
</p>
<!-- 
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
{/if} -->

<div id="collage" style={bgstyle}>
    {#each cropped_imgs as img, index}
        <img
            src={img.url}
            alt="collage album cover"
            width={100 * (1 + index)}
            height={100 * (1 + index)}
            style={`
                top: ${200 - ((100 * (1 + index))/2)}px;
                left: ${200 - ((100 * (1 + index))/2)}px;
                transform: rotate(${index%2 == 0 ? 1 : -1 * (index * 10)}deg);
                z-index: ${1000-img.rank};
            `}
        />
    {/each}
</div>

<style lang="scss">
    #collage {
        img {
            position: absolute;
        }
    }

</style>