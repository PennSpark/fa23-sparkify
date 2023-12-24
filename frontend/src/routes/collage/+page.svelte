<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import type { Image } from '$lib/types';

	let show: boolean = true;

	export let data: { cropped_images: Image[]; uncropped_images: Image[]; palette: number[] };

	let bgstyle = `background-color: rgb(
                ${data.palette[0]} 
                ${data.palette[1]} 
                ${data.palette[2]}
            );`;

	const getDoodles = () => {
		let doodles: string[] = [];
		let count = Math.round(Math.random() * 2) + 2;
		for (let i = 0; i < count; ++i) {
			doodles.push(`/doodles/${Math.round(Math.random() * 40)}.png`);
		}

		return doodles;
	};

	const getRandomDirection = () => (Math.random() > 0.5 ? 1 : -1);
	const getZIndexDiff = (index: number) => Math.round((index * 10) + (Math.random() * 20));

	const getCroppedWidth = (index: number) => 110 * Math.log(index + 10);
	const getCroppedHeight = (index: number) => 110 * Math.log(index + 10);
	const getCroppedCenter = (index: number) => 200 - getCroppedWidth(index) / 2;
	const getCroppedTilt = (index: number) => (index % 2 == 0 ? 1 : -1) * (index * Math.random() * 15);
	const getCroppedXDisplacement = (index: number) => (index % 2 == 0 ? 1 : -1) * ((index+1) * Math.random() * 50);
	const getCroppedYDisplacement = (index: number) => (index % 2 == 0 ? 2 : -1) * ((index+1) * Math.random() * 20);

	const getUncroppedWidth = (index: number) => 80 * Math.log(index + 5);
	const getUncroppedHeight = (index: number) => 80 * Math.log(index + 5);
	const getUncroppedCenter = (index: number) => 200 - getUncroppedWidth(index) / 2;
	const getUncroppedXDisplacement = () => getRandomDirection() * (Math.random() * 120);
	const getUncroppedYDisplacement = () => getRandomDirection() * (Math.random() * 120);
</script>

<svelte:head>
	<title>Your Collage | Sparkify</title>
</svelte:head>

<h1>Here's your <b>Music Collage!</b></h1>

<div class="border">
	<div id="collage" style={bgstyle}>
		{#if show}
			{#each data.cropped_images as img, index}
				<img
					src={img.url}
					alt="cropped collage album cover"
					width={getCroppedWidth(index)}
					height={getCroppedHeight(index)}
					style={`
                        top: ${getCroppedCenter(index) + getCroppedYDisplacement(index)}px;
                        left: ${getCroppedCenter(index) + getCroppedXDisplacement(index)}px;
                        transform: rotate(${getCroppedTilt(index)}deg);
                        z-index: ${1000 - getZIndexDiff(index)};
                    `}
				/>
			{/each}
			{#each data.uncropped_images as img, index}
				<img
					src={img.url}
					alt="cropped collage album cover"
					width={getUncroppedWidth(index)}
					height={getUncroppedHeight(index)}
					style={`
                        top: ${getUncroppedCenter(index) + getUncroppedYDisplacement()}px;
                        left: ${getUncroppedCenter(index) + getUncroppedXDisplacement()}px;
                        z-index: ${500 - getZIndexDiff(index)};
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
	<Button
		on:click={() => {
			show = false;
			setTimeout(() => {
				show = true;
			}, 10);
		}}>Regenerate</Button
	>
	<span style="width: 24px;" />
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
