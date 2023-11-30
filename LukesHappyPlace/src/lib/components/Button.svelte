<script lang="ts">
	import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
	const click = () => dispatch("click");
</script>

<button on:click|preventDefault={click}>
	<slot />
</button>

<style lang="scss">
    button {
        color: $black;
        border: none;
        background-color: $green;
        font-weight: 600;
        text-decoration: none;
        padding: 12px 25px;
        border-radius: 5px;

        &:hover {
			filter: drop-shadow(3px 3px 3px black);
            cursor: pointer;
		}
    }
</style>
