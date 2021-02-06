<template>
  <v-container>
    <v-card>
      <v-card-title class="ma-0 pa-0 ml-2"> Discord poll results: </v-card-title>

      <v-progress-linear
        v-for="vote in vote_list"
        v-bind:key="vote.message_id"
        background-opacity="0"
        height="25"
        color="#7289da"
        :value="(vote.votes / vote_list[0].votes) * 100"
        @click="goto_game(vote)"
      >
        <template v-slot:default>
          <div class="px-1" style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap; cursor: pointer">
            {{ vote.votes }} votes - {{ vote.name }}
          </div>
          <v-spacer></v-spacer>
        </template>
      </v-progress-linear>
    </v-card>
  </v-container>
</template>

<script>
function comparator(a, b) {
  if (a["votes"] < b["votes"]) return 1;
  if (a["votes"] > b["votes"]) return -1;
  return 0;
}

export default {
  data: () => ({
    votes: {},
    vote_list: [],
  }),

  mounted() {
    this.socket = this.$nuxtSocket({
      channel: "/gamevotes",
      persist: true,
    });
    this.socket.on("votes_discord", (msg, cb) => {
      const partial = msg.partial;
      if (partial) {
        this.votes[msg.message_id] = msg;
      } else {
        this.votes = msg;
      }

      var _vote_list = [];
      for (var key in this.votes) {
        var vote_data = { message_id: key, name: this.votes[key].game, votes: this.votes[key].yay, voters: this.votes[key].yay_voters };
        if (vote_data.votes > 0) {
          _vote_list.push(vote_data);
        }
      }

      _vote_list.sort(comparator);
      this.vote_list = _vote_list;
      this.$store.commit("set_discord_games", _vote_list);
    });
    this.socket.on("latest_pitches", (msg, cb) => {
      this.$store.commit("set_latest_pitches", msg);
    });

    this.socket.emit("votes_pls", "discordvotes");
  },
  methods: {
    goto_game: async function (game) {
      this.$router.push({
        path: "/game_discord/" + game.message_id,
      });
    },
  },
};
</script>