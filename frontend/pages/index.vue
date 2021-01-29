<template>
  <v-row justify="center" align="center">
    <v-col cols="12" md="6">
      <v-card>
        <v-card-title class="headline">Read this:</v-card-title>
        <v-card-text class="text-center">
          <p class="text-h5 font-weight-bold">
            <span style="color: red">New:</span> People with more than 100 posts in #dragons-den before Jan 27 can now vote as well.
          </p>
          <p class="text-h5 font-weight-bold">The voting here is unofficial and just to gauge interest.</p>
          <p class="text-h5 font-weight-bold">You can vote on more than one game.</p>
          <p class="text-h6 font-weight-bold">You can add any game to the list by searching for it and voting on it.</p>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col>
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
