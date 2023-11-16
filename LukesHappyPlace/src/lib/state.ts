import { get, readable } from "svelte/store";
import { generateRandomString } from "./utils";

const state = readable(generateRandomString(16));

export default function getState() {
    return get(state);
}
