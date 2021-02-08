<template>
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
            <div class="d-flex ml-0 pl-0">
              <v-img
                v-if="item.name.toLowerCase().includes('a bomb')"
                style="position: absolute; margin-top: -15px; margin-left: -45px"
                max-height="60"
                max-width="60"
                src="https://cdn.discordapp.com/attachments/666328917237563419/808083562766794822/bombchan_sans_body_or_bg.png"
              ></v-img>
              <v-img
                v-if="item.name.toLowerCase().includes('dragon angel')"
                style="position: absolute; margin-top: -15px; margin-left: -30px"
                max-height="60"
                max-width="60"
                src="https://cdn.discordapp.com/attachments/648620063045189656/808196974859124756/dragon_angel.png"
              ></v-img>
              <span v-if="item.name.toLowerCase().includes('a bomb')" class="pl-3"></span>
              <span v-if="item.name.toLowerCase().includes('dragon angel')" class="pl-8"></span>
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
</template>

<script>
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
  props: {
    vote_list: {
      type: Array,
      default: [],
    },
  },
  data: () => ({
    headers: [
      { text: "votes", value: "votes", width: "80px" },
      { text: "game", value: "name" },
    ],
  }),
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

      var color = this.dark_mode ? "#21357d" : "#7289da";
      if (vote.name) {
        if (vote.name.toLowerCase().includes("a bomb")) color = this.dark_mode ? "#692323" : "#da9090";
        if (vote.name.toLowerCase().includes("dragon angel")) color = this.dark_mode ? "#3e7d21" : "#7cda72";
      }

      return {
        "background-image": `linear-gradient(to right,${color} ${percent}%,transparent ${percent}%)`,
      };
    },
  },
  computed: {
    dark_mode: {
      get() {
        return this.$store.state.localStorage.dark_mode;
      },
      set(value) {},
    },
  },
};
</script>