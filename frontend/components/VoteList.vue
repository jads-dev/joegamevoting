<template>
  <v-col class="ma-0 pa-0">
    <v-data-table dense hide-default-footer :headers="_headers" :hide-default-header="hide_header" :items="vote_list" :items-per-page="700" class="elevation-1">
      <template v-slot:body="{ items }">
        <tbody>
          <tr v-for="item in items" :key="item.message_id" style="cursor: pointer" :style="get_row_style(item)" @click="goto_game(item)">
            <td style="max-width: 2em; width: 2em; text-overflow: clip" v-if="item.rank" class="pl-2">{{ item.rank }}</td>
            <td style="min-width: 85px; width: 85px">
              <v-row v-if="item.downvotes == 0">
                <v-img v-if="show_emojis" max-width="25" class="mr-1" :src="get_emoji_url(item.emote, item.emote_unicode)"></v-img>
                <span v-if="item.message_id != '69'">x {{ item.votes }}</span>
              </v-row>

              <v-menu v-if="item.downvotes > 0" open-on-hover right class="ma-0 pa-0">
                <template v-slot:activator="{ on, attrs }">
                  <v-row v-bind="attrs" v-on="on">
                    <v-img v-if="show_emojis" max-width="25" :src="get_emoji_url(item.emote, item.emote_unicode)"></v-img>
                    <span> x {{ item.absolute }} </span>
                  </v-row>
                </template>
                <div :style="{ 'background-color': get_row_color(item) }" class="pa-1">
                  <div class="d-flex">
                    <v-img max-width="25" :src="get_emoji_url(item.emote, item.emote_unicode)"></v-img>
                    <span>x {{ item.votes }}</span>
                  </div>
                  <div class="d-flex">
                    <v-img max-width="25" :src="get_emoji_url(item.emote2, item.emote2_unicode)"></v-img>
                    <span>x {{ item.emote2_count }}</span>
                  </div>
                  <div class="d-flex" v-for="emote in item.extra_emotes" :key="`${item.message_id}-${emote.emote}`">
                    <v-img max-width="25" :src="get_emoji_url(emote.emote, emote.emote_unicode)"></v-img>
                    <span>x {{ emote.count }}</span>
                  </div>
                </div>
              </v-menu>
            </td>
            <td class="pl-0">
              <div class="d-flex ml-0 pl-0">
                <v-img
                  v-if="item.message_id == '807293645057163285'"
                  style="position: absolute; margin-top: -25px; margin-left: -30px"
                  max-height="80"
                  max-width="80"
                  src="https://cdn.discordapp.com/attachments/666328917237563419/808083562766794822/bombchan_sans_body_or_bg.png"
                ></v-img>
                <v-img
                  v-if="item.message_id == '807297543825653801'"
                  style="position: absolute; margin-top: -25px; margin-left: -25px"
                  max-height="100"
                  max-width="100"
                  src="https://cdn.discordapp.com/attachments/648620063045189656/808196974859124756/dragon_angel.png"
                ></v-img>
                <span v-if="item.message_id == '807297543825653801'" style="padding-left: 75px"></span>
                <span v-if="item.message_id == '807293645057163285'" class="pl-12"></span>

                <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
                  <span v-if="item.weeb_status && show_weeb_status">({{ item.weeb_status }})</span> {{ item.name }}
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </template>
    </v-data-table>
  </v-col>
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
  "⬇️": "https://discord.com/assets/31abf4145cf7c27ea0e1a2e4328283fd.svg",
  "💙": "https://discord.com/assets/e37c985edda06b7d5f4559bc838c1bde.svg",
  "🔺": "https://discord.com/assets/79e14ae0b5c616e7ceb92e5c01a42cbc.svg",
  // "🟣": "https://discord.com/assets/d5705ac7e416d39813ddf63c8d396102.svg",
  "🟣": "https://discord.com/assets/a66029551e6622ee220b35677db15d8b.svg",
  "🟨": "https://discord.com/assets/0ca363e545e2f490cf4b852f5c8e0404.svg",
  "📗": "https://discord.com/assets/2f62701a0bd9896f10ba600e9bb3ee6d.svg",
  "🙏": "https://discord.com/assets/1904291ab1aa5d14b2adaaff23a578dd.svg",
  "🫂": "https://discord.com/assets/16e50cf15d1cfdc28964072544f55043.svg",
  "👎": "https://discord.com/assets/66e3cbf517993ee5261f23687a2bc032.svg",
  "👇": "https://discord.com/assets/985bb2d2398be71e1b68bc7e2103c993.svg",
  "🔆": "https://discord.com/assets/d3d76c82a46964a19a8c96e222bd414a.svg",
};
export default {
  props: {
    vote_list: {
      type: Array,
      default: [],
    },
    hide_header: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    headers: [
      { text: "", value: "rank", width: "2em" },
      { text: "votes", value: "absolute", width: "3em" },
      { text: "game", value: "name" },
    ],
    votos_seconds: 0,
    votos_minutes: 0,
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
    get_row_color: function (vote) {
      var color = this.dark_mode ? "#21357d" : "#7289da";
      if (vote.name) {
        if (vote.message_id == "807293645057163285") {
          color = this.dark_mode ? "#692323" : "#da9090";
        }
        if (vote.message_id == "807297543825653801") {
          color = this.dark_mode ? "#3e7d21" : "#7cda72";
        }
        // if (vote.message_id == "807307201949204520") {
        //   color = this.dark_mode ? "#949425" : "#dada72";
        // }
      }
      if (vote.name.toLowerCase().includes("hellgate")) {
        color = this.dark_mode ? "#7d2121" : "#da7272";
      }
      return color;
    },
    get_border_class: function (vote) {
      return {
        "gold-top": vote.rank == 1 || vote.rank == "M" || vote.rank == -5,
        "gold-mid": (vote.rank >= 1 && vote.rank <= 3) || vote.rank == "M" || (vote.rank >= -5 && vote.rank <= -1),
        "gold-bottom": vote.rank == 3 || vote.rank == "M" || vote.rank == -1,
      };
    },
    get_row_style: function (vote) {
      var background_image = undefined;
      var height = undefined;

      if (vote.message_id == "809130993507237919") {
        const max_value = 440;

        var color = this.get_row_color(vote);
        const steps = [50, 100, 100, 150];
        const overflow = steps.reduce((a, b) => a + b, 0);
        var steps_str = "";

        var percent = 0;
        var last_percent = 0;
        var cur_total = 0;
        const votes = vote.absolute;
        // const votes = 600;

        for (var i in steps) {
          const step = steps[i];
          cur_total += step;

          if (votes >= cur_total) {
            percent += (step / max_value) * 100;
            steps_str += `, ${color} ${last_percent}% ${percent}%, orange ${percent}% ${percent + 1}%`;
          } else if (votes < cur_total && votes > cur_total - step) {
            percent += (step / max_value) * 100;
            var middle = percent - ((cur_total - votes) / max_value) * 100;
            steps_str += `, ${color} ${last_percent}% ${middle}%, transparent ${middle + 1}% ${percent}%, orange ${percent}% ${percent + 1}%`;
          } else if (votes < overflow) {
            percent += (step / max_value) * 100;

            steps_str += `, transparent ${last_percent}% ${percent}%, orange ${percent}% ${percent + 1}%`;
          }

          percent += 1;
          last_percent = percent;
        }
        if (votes > overflow) {
          var step = max_value - overflow;
          cur_total += step;
          percent += (step / max_value) * 100;
          var middle = percent - ((cur_total - votes) / max_value) * 100;

          steps_str += `, red ${last_percent}% ${middle}%, transparent ${middle + 1}% ${percent}%`;
        }

        steps_str += `, transparent ${last_percent - 1}% 100%`;

        background_image = `linear-gradient(to right${steps_str})`;
      } else if (vote.message_id == "810207947661508608") {
        const percent = (vote.absolute / 350) * 100;
        var color = this.get_row_color(vote);
        background_image = `linear-gradient(to right,${color} ${percent}%,transparent ${percent}%)`;
      } else {
        const percent = (vote.absolute / this.vote_list[0].absolute) * 100;
        const color = this.get_row_color(vote);
        const color2 = this.dark_mode ? "#3b63ed" : "#b0c1ff";
        const color3 = this.dark_mode ? "#101c48" : "#4d5d96";

        if (percent >= 0) background_image = `linear-gradient(to right,${color} ${percent}%,transparent ${percent}%)`;
        else if (percent < -200) background_image = `linear-gradient(to right,${color2} ${percent + 200}%,${color3} ${percent + 200}%)`;
        else if (percent < -100) background_image = `linear-gradient(to right,${color} ${percent + 200}%,${color2} ${percent + 200}%)`;
        else background_image = `linear-gradient(to right,transparent ${percent + 100}%,${color} ${percent + 100}%)`;
      }

      if (vote.downvotes > 0) {
        // height = "50px";
      }
      if (vote.message_id == "807297543825653801" || vote.message_id == "807293645057163285") height = "50px";

      return {
        "background-image": background_image,
        height: height,
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
    _headers: {
      get() {
        return this.headers.filter((header) => header.value != "rank" || (this.vote_list.length > 0 && this.vote_list[0].rank));
      },
      set(value) {},
    },
    votos_time: {
      get() {
        this.votos_minutes = 0;
        this.votos_seconds = 0;
        return this.$store.state.votos_time;
      },
      set(value) {},
    },
    show_weeb_status: {
      get() {
        return this.$store.state.localStorage.show_weeb_status;
      },
      set(value) {
        this.$store.commit("localStorage/set_show_weeb_status", value);
      },
    },
    show_emojis: {
      get() {
        return this.$store.state.localStorage.show_emojis;
      },
      set(value) {
        this.$store.commit("localStorage/set_show_emojis", value);
      },
    },
  },
  created() {
    this.votos_timer = setInterval(
      function () {
        const delta = new Date() - new Date(this.votos_time);
        this.votos_minutes = parseInt(delta / 1000 / 60);
        this.votos_seconds = parseInt((delta / 1000) % 60);
      }.bind(this),
      1000
    );
  },
};
</script>

<style>
.v-data-table-header > tr > th {
  padding: 0 !important;
}

.v-data-table__wrapper table {
  border-collapse: collapse;
}

.gold-top {
  border-top: 1px double #d4af37;
}
.gold-mid {
  border-left: 1px double #d4af37;
  border-right: 1px double #d4af37;
}
.gold-bottom {
  border-bottom: 1px double #d4af37;
}
</style>