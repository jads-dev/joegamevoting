<template>
  <v-container>
    <v-card class="overflow-hidden">
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
          <v-expansion-panel-header class="ml-5"> VOTOS </v-expansion-panel-header>
          <v-expansion-panel-content>
            <vote-list :vote_list="votos" :hide_header="true"></vote-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
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
    outer_heaven: culled.outer_heaven,
    halls_ascension: culled.ascended_games,
    vote_list: [],
    culled_hell: culled.culled_games,
    double_hell: culled.double_hell_games,
    votos: [],
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
        this.votes[msg.message_id]["nay"] = msg["nay"];
        this.votes[msg.message_id]["game"] = msg["game"];
      } else {
        this.votes = msg;
      }

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
        };

        if (vote_data.message_id == "809130993507237919") {
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
    });
    this.socket.on("latest_pitches", (msg, cb) => {
      this.$store.commit("set_latest_pitches", msg);
    });

    this.socket.emit("votes_pls", "discordvotes");
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
