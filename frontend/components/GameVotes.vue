<template>
  <v-container>
    <v-card>
      <v-card-title class="ma-0 pa-0 ml-2"> Unofficial poll results: </v-card-title>
      <v-progress-linear
        v-for="vote in votes"
        v-bind:key="vote.game_id"
        background-opacity="0"
        height="25"
        :value="(vote.votes / votes[0].votes) * 100"
        @click="goto_game(vote)"
      >
        <template v-slot:default>
          <v-tooltip top open-delay="200">
            <template v-slot:activator="{ on, attrs }">
              <div v-bind="attrs" v-on="on" class="px-1" style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap; cursor: pointer">
                {{ vote.votes }} votes - {{ vote.name }}
              </div>
            </template>
            <span>{{ vote.name }}</span>
          </v-tooltip>
          <v-spacer></v-spacer>
        </template>
      </v-progress-linear>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    votes: [],
  }),

  mounted() {
    this.socket = this.$nuxtSocket({
      channel: "/gamevotes",
      persist: true,
    });
    this.socket.on("votes", (msg, cb) => {
      this.votes = msg;
    });
    this.socket.emit("votes_pls", "fanvotes");
  },
  methods: {
    goto_game: async function (vote) {
      this.$router.push({
        path: "/game/" + vote.game_id,
      });
    },
  },
};
</script>