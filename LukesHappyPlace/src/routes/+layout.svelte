<script>
	import '../app.scss';
</script>

<header>
	<a href="/">Our Happy Place</a>
	<nav>
		<a href="/">Home</a>
		<a href="/about">About</a>
		<a href="/contact">Contact</a>
	</nav>
</header>

<main>
	<slot />
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
