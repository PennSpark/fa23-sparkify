<script lang="ts">
    export let href: string;
</script>

<a
    {href}
>
    <slot />
</a>

<style lang="scss">
    a {
        color: $black;
        background-color: $green;
        font-weight: 600;
        text-decoration: none;
        padding: 12px 25px;
        border-radius: 5px;

        &:hover {
			filter: drop-shadow(3px 3px 3px black);
		}
    }
</style>