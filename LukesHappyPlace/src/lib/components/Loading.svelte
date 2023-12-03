<script lang="ts">
	export let time: number;
</script>

<div class="loading">
	<h2>We got your data!</h2>
	<p>
		It takes a while to generate the collage...
		<br />
		Please hold tight!
	</p>
	<div class="progress">
		<div class="line" style={`width: ${(100 * (3000 - time)) / 3000}%`} />
	</div>
</div>

<style lang="scss">
	.loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		h2 {
			font-size: 2em;
			font-weight: 400;
		}
		p {
			font-size: 1.2em;
			margin-block: 6vh;
		}
		.progress {
			display: block;
			background-color: #303030;
			width: 50vw;
			height: 15px;
			border-radius: 10px;
			.line {
				background-color: $green;
				height: 15px;
				border-radius: 10px;
			}
		}
	}
</style>
