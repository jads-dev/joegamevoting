<template>
  <v-container>
    <v-card>
      <v-card-title class="ma-0 pa-0 ml-2"> Discord poll results: </v-card-title>
      <v-data-table dense hide-default-footer :headers="headers" :items="vote_list" :items-per-page="700" class="elevation-1">
        <template v-slot:body="{ items }">
          <tbody>
            <tr v-for="item in items" :key="item.message_id" style="cursor: pointer" v-bind:style="get_bg_style(item)" @click="goto_game(item)">
              <td>
                <v-row>
                  <v-img max-width="25" class="mr-1" :src="get_emoji_url(item.emote, item.emote_unicode)"></v-img>
                  <span>x {{ item.votes }}</span>
                </v-row>
              </td>
              <td>
                <div class="d-flex">
                  <v-img
                    v-for="emote in item.extra_emotes"
                    :key="`${item.message_id}-${emote.emote}`"
                    max-width="25"
                    :src="get_emoji_url(emote.emote, emote.emote_unicode)"
                  ></v-img>
                  <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{ item.name }}</div>
                </div>
              </td>
            </tr>
          </tbody>
        </template>
      </v-data-table>
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
  "✂️": "https://discord.com/assets/3dcc54fffb253571d6eab25020e424f5.svg",
};

export default {
  data: () => ({
    votes: {},
    vote_list: [],
    headers: [
      { text: "votes", value: "votes", width: "80px" },
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
        this.votes[msg.message_id]["game"] = msg["game"];
      } else {
        this.votes = msg;
      }

      var _vote_list = [];
      for (var key in this.votes) {
        console.log(this.votes[key].extra_emotes);
        var vote_data = {
          message_id: key,
          name: this.votes[key].game,
          votes: this.votes[key].yay,
          emote: this.votes[key].emote,
          emote_unicode: this.votes[key].emote_unicode,
          extra_emotes: this.votes[key].extra_emotes,
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
    get_bg_style: function (vote) {
      const percent = (vote.votes / this.vote_list[0].votes) * 100;
      var color = "#7289da";
      if (vote.message_id == 807293645057163285) color = "#da9090";
      if (vote.message_id == 807297543825653801) color = "#7cda72";

      return { "background-image": `linear-gradient(to right,${color} ${percent}%,transparent ${percent}%)` };
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