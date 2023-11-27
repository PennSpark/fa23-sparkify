<script lang="ts">
    export let time: number;
</script>

<div class="loading">
    <h2>We got your data!</h2>
    <p>
        It takes a while to generate the collage...
        <br />Please hold tight!
    </p>
    <p>{100 - time}%</p>
</div>
