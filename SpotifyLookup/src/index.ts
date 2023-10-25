import { getTopTracks } from "./queries";

async function test() {
  let top_tracks = await getTopTracks(5);

  await console.log(top_tracks);
}

test();
