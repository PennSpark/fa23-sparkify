<script>
	import { navigating } from '$app/stores';
	import Loading from '$lib/components/Loading.svelte';
	import '../app.scss';

	let time = 100; // 10 seconds

	setInterval(() => {
		if(time > 0) {
			if($navigating) {
				time--;
			}
		}
	}, 10)
</script>

<header>
	<a href="/">Sparkify</a>
	<nav>
		<a href="/">Home</a>
		<a href="/about">About</a>
		<a target="_blank" rel="noopener noreferrer" href="https://pennspark.org/">Contact</a>
	</nav>
</header>

<main>
	{#if $navigating}
		<Loading time={time} />
	{:else}
		<slot />
	{/if}
</main>

<style lang="scss">
	header {
		padding: 20px;
		font-weight: 600;
		font-size: 1.2em;
		nav {
			display: inline;
			float: right;
			a {
				color: $white;
				text-decoration: none;
				padding-inline: 20px;
				&:hover {
					color: $green;
				}
			}
		}
	}
	main {
		margin-inline: 10vw;
		justify-content: center;
	}
</style>
