<script lang="ts">
    import output from "./output.json";
	import Button from "$lib/components/Button.svelte";
	import type { Artist, Track } from "$lib/types";

    export let data: { expired: boolean, tracks: Track[], artists: Artist[] };
    
    let bgstyle = `background-color: rgb(
                ${output.dominant_color[0]} 
                ${output.dominant_color[1]} 
                ${output.dominant_color[2]}
            );`;

    const cropped_imgs = output.cropped_image_data.sort((a,b) => {
        return a.rank - b.rank;
    });
</script>

<svelte:head>
	<title>Your Collage | Sparkify</title>
</svelte:head>


{#if data.tracks.length === 0 && data.artists.length === 0}
    <a href="/auth/login">LOGIN</a>
{:else}
    <h1>Here's your <b>Music Collage!</b></h1>
    <div class="border">
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
    </div>
    <div id="buttons">
        <Button href="#">Regenerate</Button>
        <span style="width: 24px;"></span>
        <Button href="#">Share</Button>
    </div>
{/if}

<style lang="scss">
    h1 {
        text-align: center;
        font-weight: 400;
        b {
            color: $green;
        }
    }
    .border {
        position: relative;
        padding: 16px;
        width: 420px;
        margin-inline: auto;
        background-color: #303030;
        margin-block: 3vh;
    }
    #collage {
        position: relative;
        margin-inline: auto;
        width: 400px;
        height: 400px;
        overflow: hidden;
        img {
            position: absolute;
        }

        border: $white 10px solid;
        box-shadow: 0px 0px 14px 3px $black;
    }
    #buttons {
        display: flex;
        justify-content: center;
    }
</style>