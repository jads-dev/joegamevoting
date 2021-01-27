<template>
  <v-row justify="center" align="center">
    <v-col cols="6">
      <div class="text-center"></div>
      <v-card>
        <v-card-title class="headline">What's this? </v-card-title>
        <v-card-text>
          <p>
            This website is for people to vote on which game they would like for Joe to play on stream. This page is not officially endorsed by Joe (I haven't
            asked him) and should be treated as a fan page.
          </p>
          <p>
            On the left there should be a descending list of what people have voted on, this should be updated in real time. You can click on the games there to
            visit it's page and cast your own vote or use the search bar above. You can vote on more than one game. Votes are <b>NOT</b> anonymous.
          </p>
          <p>
            The available game list was fetched from igdb.com and does not include every game (like re-releases/remasters/collections/etc.) if there's a big one
            missing, you can ping me on discord
          </p>
          <p>Voting is restricted to people that have the twitch or patreon roles on discord. This is done to limit people manipulating votes with bots/etc.</p>
          <p>The site is probably a bit rough around the edges, but should be at the very minimum functional :P</p>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {};
</script>
