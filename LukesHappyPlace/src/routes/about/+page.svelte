<svelte:head>
	<title>About | Sparkify</title>
</svelte:head>

<h1>About</h1>
<h3>
	Created as a
	<a target="_blank" rel="noopener noreferrer" href="https://pennspark.org/">Penn Spark</a>
	Fall 2023 Red Project, Sparkify is a web app that allows users to create a collage of their top artists
	and tracks on Spotify.
</h3>

<p>
	Here are some of the decisions the design team made in order to most effectively visualize one’s music taste.
	Album selection: We opted to select albums with identifiable subjects, as they would be most notable when cropped and placed on the collage.
	Collage Background:  We decided to select the most common light/dark color represented across the albums as the main background color. Additionally, accent colors were chosen by finding the contrasting color of the main background color.
	Album placement: We chose to arrange the albums by listening frequency. Those albums with the most listens are placed in the foreground and center of the collage. As the frequency of listens decreases, the albums move radially outward and get placed further into the background of the collage. Additionally, the uncropped images are placed furthest in the background.
</p>

<ul>
	<li>Nwai Alfa</li>
	<li>Matthew Cho</li>
	<li>Paul Loh</li>
	<li>Sonia Tam</li>
	<li>Luke Tong</li>
	<li>Jasmine Wang</li>
</ul>

<style lang="scss">
	ul {
		padding-top: 10vh;
		list-style-type: none;
		li {
			font-size: 1.2em;
			padding-bottom: 1vh;
		}
	}
</style>
