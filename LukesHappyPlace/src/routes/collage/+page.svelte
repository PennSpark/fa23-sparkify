<script lang="ts">
	import Button from "$lib/components/Button.svelte";

    let show: boolean = true;

    export let data: { images: string[] };

    console.log(data);
    
    // let bgstyle = `background-color: rgb(
    //             ${output.dominant_color[0]} 
    //             ${output.dominant_color[1]} 
    //             ${output.dominant_color[2]}
    //         );`;
   let bgstyle = `background-color: #1E1F27`;

    // // descending order TODO: CHANGE THIS TO a.rank - b.rank
    // const cropped_imgs = output.cropped_image_data.sort((a,b) => {
    //     return b.rank - a.rank;
    // });

    // // descending order
    // const uncropped_imgs = output.uncropped_image_data.sort((a, b) => {
    //     return a.rank - b.rank;
    // })

    const getDoodles = () => {
        let doodles: string[] = [];
        let count = Math.round(Math.random() * 2) + 2;
        for(let i = 0; i < count; ++i) {
            doodles.push(`/doodles/${Math.round(Math.random() * 40)}.png`);
        }

        return doodles;
    }

    const getRandomDirection = () => Math.random() > 0.5 ? 1 : -1;

    const getCroppedWidth = (index: number) => 110 * (Math.log(index + 10));
    const getCroppedHeight = (index: number) => 110 * (Math.log(index + 10));
    const getCroppedCenter = (index: number) => 200 - (getCroppedWidth(index)/2);
    const getCroppedTilt = (index: number) => (index%2 == 0 ? 1 : -1) * (index * 10);
    const getCroppedXDisplacement = (index: number) => (index % 2 == 0 ? 1 : -1) * (index * 40);
    const getCroppedYDisplacement = (index: number) => (index % 2 == 0 ? 2 : -1) * (index * 15);

    const getUncroppedWidth = (index: number) => 80 * (Math.log(index + 5));
    const getUncroppedHeight = (index: number) => 80 * (Math.log(index + 5));
    const getUncroppedCenter = (index: number) => 200 - (getUncroppedWidth(index)/2);
    const getUncroppedXDisplacement = (index: number) => getRandomDirection() * (Math.random() * 120);
    const getUncroppedYDisplacement = (index: number) => getRandomDirection() * (Math.random() * 120);
</script>

<svelte:head>
	<title>Your Collage | Sparkify</title>
</svelte:head>

<h1>Here's your <b>Music Collage!</b></h1>

<div class="border">
    <div id="collage" style={bgstyle}>
        {#if show}
            {#each data.images as img, index}
                <img
                    src={img}
                    alt="cropped collage album cover"
                    width={getCroppedWidth(index)}
                    height={getCroppedHeight(index)}
                    style={`
                        top: ${getCroppedCenter(index) + getCroppedYDisplacement(index)}px;
                        left: ${getCroppedCenter(index) + getCroppedXDisplacement(index)}px;
                        transform: rotate(${getCroppedTilt(index)}deg);
                        z-index: ${1000-index};
                    `}
                />
            {/each}
            {#each data.images as img, index}
                <img
                    src={img}
                    alt="cropped collage album cover"
                    width={getUncroppedWidth(index)}
                    height={getUncroppedHeight(index)}
                    style={`
                        top: ${getUncroppedCenter(index) + getUncroppedYDisplacement(index)}px;
                        left: ${getUncroppedCenter(index) + getUncroppedXDisplacement(index)}px;
                        z-index: ${100-index};
                    `}
                />
            {/each}
            {#each getDoodles() as doodle}
                <img
                    src={doodle}
                    alt="doodle"
                    width={200}
                    height={200}
                    style={`
                        top: ${Math.random() * 200}px;
                        left: ${Math.random() * 200}px;
                        z-index: 1000;
                    `}
                />
            {/each}
        {/if}
    </div>
</div>
<div id="buttons">
    <Button on:click={() => {
        show = false;
        setTimeout(() => {
            show = true;
        }, 10);
     }}>Regenerate</Button>
    <span style="width: 24px;"></span>
    <Button>Share</Button>
</div>

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