<script lang="ts">
	import Button from "$lib/components/Button.svelte";
import type { Artist, Track } from "../lib/types";

    export let data: { tracks: Track[], artists: Artist[] };
</script>

<div class="container">
    <section class="left">
        <h1>Visualize your</h1>
        <h1 class="green">Music Taste.</h1>
        <p>
            Create your unique Music
            <br />
            collage and share with friends.
        </p>
        <Button href="/collage">
            Sync with 
            <img class="spotify" src="/external/spotify.png" height=22rem alt="spotify logo">
        </Button>
    </section>
    <section class="right">
        <img class="one" width=351 height=355 src="/home/1.png" alt="Example album cover 1" />
        <img class="two" width=250 height=250 src="/home/2.png" alt="Example album cover 2" />
        <img class="three" width=280 height=280 src="/home/3.png" alt="Example album cover 3" />
        <img class="four" width=310 height=310 src="/home/4.png" alt="Example album cover 4" />
    </section>
</div>



<style lang="scss">
    .container {
        display: flex;
        flex-direction: row;
    }
    .left {
        margin-top: 20vh;
        h1 {
            font-size: 3.5em;
        }
        .green {
            color: $green;
        }
        p {
            font-size: 1.2em;
            margin-block: 6vh;
        }
        .spotify {
        }
    }
    .right {
        margin-left: 10vw;
        position: relative;
        img {
            position: absolute;
        }
        .one {
            left: 30px;
        }
        .two {
            left: 340px;
            top: 110px;
        }
        .three {
            top: 320px;
            left: 60px;
        }
        .four {
            top: 300px;
            left: 300px;
        }
    }
</style>