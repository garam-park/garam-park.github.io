import { connect } from "@dagger.io/dagger";

connect(async (client) => {
  const image = client.container().build(client.host().directory("."));
  await image.publish("ghcr.io/garam-park/blog:latest");
});
