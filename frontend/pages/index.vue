<template>
  <v-row justify="center" align="center" class="mt-4">
    <template v-if="official">
      <v-col cols="12">
        <p class="text-h4 text-center">These are the current results of the official discord poll.</p>
        <p class="text-h4 text-center">To vote you need to go to the voting channel on discord, you need to have the patreon or twitch role to access it.</p>
        <p class="text-h4 text-center">Site is a WIP and there's some stuff missing/hacky.</p>
      </v-col>
    </template>
    <template v-else>
      <v-col cols="12">
        <p class="text-h3 text-center">This is the fan poll, it is unnoficial and fanmade and doesn't affect what Joe plays on stream at all!</p>
        <p class="text-h4 text-center">You can see the results of the official discord poll by click the switch on the top left.</p>
      </v-col>
      <v-col cols="12">
        <v-card>
          <p class="text-h4 text-center pt-2">Short Version:</p>
          <v-card-text class="text-center">
            <p class="text-h5 font-weight-bold">
              You need the patron/twitch sub role on discord or have more than 100 posts in #dragons-den before Jan 27 to be able to vote.
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
              This website is for people to vote on which game they would like for Joe to play on stream, the vote is merely symbolical and doesn't affect what
              joe plays on stream. This page is not officially endorsed by Joe (I haven't asked him) and should be treated as a fan page.
            </p>
            <p>
              On the left there should be a descending list of what people have voted on, this should be updated in real time. You can click on the games there
              to visit it's page and cast your own vote or use the search bar above. You can vote on more than one game. Votes are <b>NOT</b> anonymous.
            </p>
            <p>
              The available game list was fetched from igdb.com and does not include every game (like re-releases/remasters/collections/etc.) if there's a big
              one missing, you can ping me on discord
            </p>
            <p>
              Voting is restricted to people that have the twitch or patreon roles on discord. This is done to limit people manipulating votes with bots/etc. If
              you had more that 100 posts on #dragons-den before Jan 27, 2021 you can also vote.
            </p>
            <p>The site is probably a bit rough around the edges, but should be at the very minimum functional :P</p>
          </v-card-text>
        </v-card>
      </v-col>
    </template>
  </v-row>
</template>

<script>
export default {
  computed: {
    official: {
      get() {
        return this.$store.state.localStorage.official;
      },
      set(value) {},
    },
  },
};
</script>
