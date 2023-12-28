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
	We generated the thought with the intention of adding more flavors to Spotify-wrapped. 
	After considering various formats, we decided on the collage as it offers an artistic 
	and shareable expression. But how to ask codes to create collage for us?
</p>
<ul>
	<li>
		1. The designers began by creating collages, actively taking notes on the steps and the "factors" that contribute to a "good collage work" (very subjective!).
	</li>
	<li>
		2. The designers then tried to synthesize the steps and express them in well-structured specific instructions.
	</li>
	<li>
		3. The designers passed the text instructions to developers, who play an essential role in the project and are responsible for bringing everything to life in code.
	</li>
</ul>

<p>
	<b>For those who are curious about our design decisions:</b>
</p>

<ul>
	<li>
		<b>Album selection:</b> We opted to select albums with identifiable subjects, as they would be most notable when cropped and placed on the collage.
	</li>
	<li>
		<b>Collage Background:</b> We decided to select the most common light/dark color represented across the albums as the main background color. Additionally, accent colors were chosen by finding the contrasting color of the main background color. 
	</li>
	<li>
		<b>Album placement:</b> We chose to arrange the albums by listening frequency. Those albums with the most listens are placed in the foreground and center of the collage. As the frequency of listens decreases, the albums move radially outward and get placed further into the background of the collage. Additionally, the uncropped images are placed furthest in the background.
	</li>
</ul>

<style lang="scss">
	h3 {
		padding-block: 5vh;
		a {
			color: $green;
			text-decoration: underline;
		}
	}
	p {
		font-size: 1.2em;
	}
	ul {
		padding-bottom: 5vh;
		list-style-type: none;
		li {
			font-size: 1.2em;
			padding-block: 2vh;
		}
	}
</style>
