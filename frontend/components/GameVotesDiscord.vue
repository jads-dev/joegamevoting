<template>
  <v-container>
    <v-card>
      <v-card-title class="ma-0 pa-0 ml-2"> Discord poll results: </v-card-title>
      <v-data-table dense hide-default-footer :headers="headers" :items="vote_list" :items-per-page="700" class="elevation-1" @click:row="goto_game">
        <template v-slot:[`item.votes`]="{ item }">
          <v-row>
            <v-img max-width="25" class="mr-1" :src="get_emoji_url(item.emote, item.emote_unicode)"></v-img>
            <span>x {{ item.votes }}</span>
          </v-row>
        </template>
        <template v-slot:[`item.name`]="{ item }">
          {{ item.name }}
        </template>
      </v-data-table>
      <!-- <v-progress-linear
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
      </v-progress-linear> -->
    </v-card>
  </v-container>
</template>

<script>
function comparator(a, b) {
  if (a["votes"] < b["votes"]) return 1;
  if (a["votes"] > b["votes"]) return -1;
  return 0;
}

var emoji_urls = {
  "🏘️": "https://discord.com/assets/912a52fc3c152af29923ca7e9ae043b0.svg",
  "😴": "https://discord.com/assets/711ac22a92d00f844023ded91f820e8c.svg",
  "🐦": "https://discord.com/assets/cf725f98edb284d25530f5dbd7d30ee4.svg",
  "🔥": "https://discord.com/assets/67069a13e006345ce28ecc581f2ed162.svg",
  "🌰": "https://discord.com/assets/07e63adc84f2b773c10ee339a8fcbf8c.svg",
  "👍": "https://discord.com/assets/08c0a077780263f3df97613e58e71744.svg",
  "🤡": "https://discord.com/assets/19fc9fc6001951c7370b1fd74e1570f1.svg",
  "🌩️": "https://discord.com/assets/bc55d554d8c7432189439e0edd242bef.svg",
  "🥛": "https://discord.com/assets/c7b9a045336a335d4b87fae6b75b73ce.svg",
  "😆": "https://discord.com/assets/babfa5ab2aa87f7001ac9c1f9a7d5f34.svg",
  "🍑": "https://discord.com/assets/1799c138d1fe59c90b621531822b0be2.svg",
  "👻": "https://discord.com/assets/d92e0fd8dd2558af60d2a77eaae3100f.svg",
  "🔛": "https://discord.com/assets/b8b439115436db0c0bbff081749a1ddb.svg",
  "🧠": "https://discord.com/assets/0bf5972bff8b8b4c26621bd5cd25d839.svg",
  "🇫": "https://discord.com/assets/197cdfb70e6835c81cbb1af86ab7e01e.svg",
  "🎈": "https://discord.com/assets/a6298512f50632252a23cc264ec73f29.svg",
  "🦈": "https://discord.com/assets/7141e059d1cd75465ac7cdfa2101da72.svg",
};

export default {
  data: () => ({
    votes: {},
    vote_list: [],
    headers: [
      { text: "votes", value: "votes", width: "75px" },
      { text: "game", value: "name" },
    ],
  }),

  mounted() {
    this.socket = this.$nuxtSocket({
      channel: "/gamevotes",
      persist: true,
    });
    this.socket.on("votes_discord", (msg, cb) => {
      const partial = msg.partial;
      if (partial) {
        this.votes[msg.message_id]["yay"] = msg["yay"];
      } else {
        this.votes = msg;
      }

      var _vote_list = [];
      for (var key in this.votes) {
        var vote_data = {
          message_id: key,
          name: this.votes[key].game,
          votes: this.votes[key].yay,
          emote: this.votes[key].emote,
          emote_unicode: this.votes[key].emote_unicode,
        };
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
    get_emoji_url: function (emoji, emoji_unicode) {
      if (emoji_unicode) {
        return emoji_urls[emoji];
      } else {
        return "https://cdn.discordapp.com/emojis/" + emoji;
      }
    },
  },
};
</script>

<style >
.v-data-table--dense td {
  max-width: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>