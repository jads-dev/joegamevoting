<template>
  <v-container>
    <v-card class="overflow-hidden">
      <v-row class="mt-2 mb-1 ml-1">
        <no-ssr>
          <v-switch hide-details dense v-model="dark_mode" label="Dark Mode" class="ml-2 ma-0 pa-0"> </v-switch>
          <v-switch hide-details dense v-model="wide_mode" label="Wide Mode" class="ml-2 ma-0 pa-0"> </v-switch>
          <v-switch hide-details dense v-model="show_weeb_status" label="Show Weeb Status" class="ml-2 ma-0 pa-0"> </v-switch>
        </no-ssr>
      </v-row>

      <v-card-title class="ma-0 pa-0 ml-2"> Discord poll results: </v-card-title>
      <v-expansion-panels multiple v-model="panel">
        <v-expansion-panel>
          <v-expansion-panel-header class="ml-5"> Outer Heaven </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="outer_heaven" :hide_header="true"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header class="ml-5"> Halls of Ascension </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="halls_ascension" :hide_header="true"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header class="ml-5"> SPECIALS </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="votos" :hide_header="true"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <span v-if="has_historical_votes" style="color: red">Not Receiving Vote Updates</span>
        <span v-if="has_historical_votes" style="color: red">Not Receiving Vote Updates</span>
        <v-expansion-panel>
          <v-expansion-panel-header class="ml-5"> The Voting Veldt </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="vote_list"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header class="ml-5"> The Hell of Culled Things </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="culled_hell"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header class="ml-5"> Double Hell </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="double_hell" :hide_header="true"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
import VoteList from "./VoteList.vue";

function comparator_votes(a, b) {
  if (a["absolute"] < b["absolute"]) return 1;
  if (a["absolute"] > b["absolute"]) return -1;
  return 0;
}
function comparator_name(a, b) {
  if (a["name"] < b["name"]) return -1;
  if (a["name"] > b["name"]) return 1;
  return 0;
}

import culled from "@/static/culled.json";
import VoteListSimple from "./VoteListSimple.vue";

export default {
  components: { VoteList, VoteListSimple },
  data: () => ({
    panel: [0, 1, 2, 3],
    votes: {},
    outer_heaven: culled.outer_heaven.sort(comparator_votes),
    halls_ascension: culled.ascended_games,
    vote_list: [],
    culled_hell: culled.culled_games,
    double_hell: culled.double_hell_games,
    votos: [],
    votes_changed: false,
  }),

  mounted() {
    this.socket = this.$nuxtSocket({
      channel: "/gamevotes",
      persist: true,
    });
    this.socket.on("votes_discord", (msg, cb) => {
      if (this.has_historical_votes) return;
      this.votes = msg;
      this.votes_changed = true;
    });

    this.socket.on("votes_discord_partial", (msg, cb) => {
      if (this.has_historical_votes) return;

      for (var i = 0; i < msg.length; i++) {
        const vote = msg[i];
        this.votes[vote.message_id]["yay"] = vote["yay"];
        this.votes[vote.message_id]["nay"] = vote["nay"];
        this.votes[vote.message_id]["game"] = vote["game"];
        this.votes[vote.message_id]["extra_emotes"] = vote["extra_emotes"];
      }

      this.votes_changed = true;
    });

    this.socket.on("latest_pitches", (msg, cb) => {
      this.$store.commit("set_latest_pitches", msg);
    });
    this.socket.on("votos_time", (msg, cb) => {
      this.$store.commit("set_votos_time", msg);
    });

    this.socket.emit("votes_pls", "discordvotes");

    this.vote_timer = setInterval(
      function () {
        if (this.votes_changed) {
          this.parse_votes();
          this.votes_changed = false;
        }
      }.bind(this),
      500
    );
  },
  methods: {
    parse_votes: async function () {
      var _vote_list = [];
      var _votos = [];
      for (var key in this.votes) {
        var vote_data = {
          message_id: key,
          name: this.votes[key].game,
          votes: this.votes[key].yay,
          downvotes: this.votes[key].nay,
          absolute: this.votes[key].yay - this.votes[key].nay,
          emote: this.votes[key].emote,
          emote_unicode: this.votes[key].emote_unicode,
          emote2: this.votes[key].emote2,
          emote2_unicode: this.votes[key].emote2_unicode,
          extra_emotes: this.votes[key].extra_emotes,
          weeb_status: this.votes[key].weeb_status,
        };

        if (
          vote_data.message_id == "809130993507237919" ||
          vote_data.message_id == "809410955880562701" ||
          vote_data.message_id == "809535003406893082" ||
          vote_data.message_id == "810207947661508608"
        ) {
          _votos.push(vote_data);
        } else if (vote_data.votes > 0) {
          _vote_list.push(vote_data);
        }
      }

      _vote_list.sort(comparator_name);
      _vote_list.sort(comparator_votes);

      var c = 0;
      for (var i = 0; i < _vote_list.length; i++) {
        if (["807296983286415411", "807291135633522789"].includes(_vote_list[i].message_id)) {
          _vote_list[i]["rank"] = "-";
        } else {
          c += 1;
          _vote_list[i]["rank"] = c;
        }
      }

      this.vote_list = _vote_list;
      this.votos = _votos;

      var _discord_games = this.outer_heaven.concat(this.halls_ascension, this.vote_list, this.culled_hell, this.double_hell, this.votos);

      this.$store.commit("set_discord_games", _discord_games);
    },
  },
  computed: {
    historical_votes: {
      get() {
        return this.$store.state.historical_votes;
      },
      set(value) {},
    },
    has_historical_votes: {
      get() {
        return Object.keys(this.historical_votes).length > 0;
      },
      set(value) {},
    },
    dark_mode: {
      get() {
        return this.$store.state.localStorage.dark_mode;
      },
      set(value) {
        this.$store.commit("localStorage/set_dark_mode", value);
      },
    },
    show_weeb_status: {
      get() {
        return this.$store.state.localStorage.show_weeb_status;
      },
      set(value) {
        this.$store.commit("localStorage/set_show_weeb_status", value);
      },
    },
    wide_mode: {
      get() {
        return this.$store.state.localStorage.wide_mode;
      },
      set(value) {
        this.$store.commit("localStorage/set_wide_mode", value);
      },
    },
  },
  watch: {
    historical_votes: function (val) {
      this.votes = val;
      this.parse_votes();
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
.v-expansion-panel-header,
.v-expansion-panel-header--active {
  padding-left: 0 !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;

  min-height: 25px !important;
}
.v-expansion-panel-content__wrap {
  padding: 0 !important;
}
</style>
