<template>
  <div>
    <v-card>
      <v-row no-gutters>
        <v-col cols="2">
          <v-img width="300px" :src="game_data.cover_url_big"></v-img>
        </v-col>
        <v-col class="xs-11">
          <v-card-title class="text-h3">
            {{ game_data.name }}
          </v-card-title>
          <v-card-subtitle class="mb-0 pb-0">
            <span class="text-overline"> {{ game_data.release_date | date }} <br /> </span>
            <span class="text-overline">
              {{ game_platforms.join(", ") }}
            </span>
          </v-card-subtitle>
          <v-card-subtitle class="mt-0 pt-0">
            <template v-if="game_data.block_level > 0">
              <v-btn disabled> can't vote </v-btn>
              <span class="ml-2">
                {{ game_data.reason }}
              </span>
            </template>
            <template v-else>
              <template v-if="game_data.can_vote">
                <v-btn v-if="!game_data.vote" dense @click="vote_game(true)" color="primary"> Vote </v-btn>
                <v-btn v-else dense @click="vote_game(false)"> Unvote </v-btn>
              </template>
              <template v-else>
                <v-btn disabled> can't vote </v-btn>
                <span v-if="!user.username" class="ml-2"> You need to login before you can vote</span>
                <span v-else class="ml-2"> You need to have the twitch sub or patreon role on discord to vote</span>
              </template>
            </template>
          </v-card-subtitle>
          <v-card-subtitle class="mt-n3 pt-0"> This is <span style="color: red; font-weight: bold">not</span> an official vote. </v-card-subtitle>
          <v-card-text>
            <div class="overflow-y-auto" style="white-space: pre-wrap; max-height: 200px">{{ game_data.summary }}</div>
          </v-card-text>
        </v-col>
      </v-row>
    </v-card>
    <v-row>
      <v-col cols="12" md="6" class="px-1">
        <v-card class="mt-2">
          <v-card-title> Why users think joe should play this game </v-card-title>
          <v-card-text>
            <v-card outlined elevation="12" v-if="game_pitches.length == 0">
              <v-card-text class="text-center"> No one has written a pitch for this game yet.</v-card-text>
            </v-card>
            <v-card
              v-for="pitch in game_pitches"
              v-bind:key="pitch.user_id"
              outlined
              class="mt-3"
              elevation="12"
              :style="pitch.pinned ? 'border: 1px solid green;' : ''"
            >
              <div class="text-center my-n3" v-if="pitch.pinned">
                <span class="px-1" :style="pitch.pinned ? 'color: green; background: #1E1E1E' : ''"> Pinned </span>
              </div>
              <v-card-text style="white-space: pre-wrap">{{ pitch.pitch }}</v-card-text>
              <v-card-title class="justify-center">
                <v-avatar left size="35">
                  <v-img :src="pitch.avatar_url" :alt="pitch.username"></v-img>
                </v-avatar>
                <span class="ml-1">{{ pitch.username }}</span>
              </v-card-title>
            </v-card>
          </v-card-text>
        </v-card>
        <v-card class="mt-2" v-if="game_data.can_pitch && game_data.can_vote">
          <v-card-text>
            <v-textarea v-model="pitch" label="Write your own pitch" counter maxlength="2000" outlined></v-textarea>
            <v-card-actions class="ma-0 pa-0">
              Warning: You're only allowed 1 pitch per game <br />
              Warning 2: Due to developer lazyness, pitches cannot be edited or deleted by the user.
              <v-spacer></v-spacer>
              <v-btn outlined dense @click="pitch_game"> send pitch </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" class="pl-1">
        <v-card class="mt-2">
          <v-card-title> Users that voted for this game </v-card-title>
          <v-card-text>
            <v-chip pill class="ml-1 mb-1" v-for="voter in game_voters" v-bind:key="voter.user_id">
              <v-avatar left>
                <v-img :src="voter.avatar_url" :alt="voter.username"></v-img>
              </v-avatar>
              {{ voter.username }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data: () => ({
    game_data: {},
    game_platforms: [],
    game_voters: [],
    game_pitches: [],
    pitch: "",
  }),
  created: async function () {
    this.$store.commit("localStorage/set_official", false);
    const game_data = await this.$axios.$get(`/api/game/${this.$route.params.id}`);
    this.game_data = game_data;

    const game_platforms = await this.$axios.$get(`/api/game/platforms/${this.$route.params.id}`);
    this.game_platforms = game_platforms.map(function (obj) {
      return obj.name;
    });

    const game_voters = await this.$axios.$get(`/api/game/${this.$route.params.id}/voters`);
    this.game_voters = game_voters;

    const game_pitches = await this.$axios.$get(`/api/game/${this.$route.params.id}/pitches`);
    this.game_pitches = game_pitches;
  },

  methods: {
    vote_game: async function (upvote) {
      var params = {
        upvote: upvote,
      };
      await this.$axios.$post(`/api/game/${this.$route.params.id}/vote`, params);
      this.game_data.vote = upvote;

      const game_voters = await this.$axios.$get(`/api/game/${this.$route.params.id}/voters`);
      this.game_voters = game_voters;
    },
    pitch_game: async function () {
      var params = {
        pitch: this.pitch,
      };
      await this.$axios.$post(`/api/game/${this.$route.params.id}/pitch`, params);

      const game_pitches = await this.$axios.$get(`/api/game/${this.$route.params.id}/pitches`);
      this.game_pitches = game_pitches;

      const game_data = await this.$axios.$get(`/api/game/${this.$route.params.id}`);
      this.game_data = game_data;
    },
  },

  filters: {
    date: function (dt) {
      if (!dt) {
        return "(n/a)";
      }
      dt = new Date(dt * 1000);
      return dt.toLocaleString("default", { month: "long" }) + " " + dt.getDate() + ", " + dt.getFullYear();
    },
  },

  computed: {
    user: {
      get() {
        return this.$store.state.localStorage.user;
      },
      set(value) {},
    },
  },

  asyncData(context) {
    return context.$axios.get(`/api/game/${context.route.params.id}`).then((res) => {
      return { game_data: res.data };
    });
  },

  head() {
    return {
      title: "Joevotes - " + this.game_data.name,
      meta: [
        {
          hid: "description",
          name: "description",
          content: this.game_data.summary.substring(0, 200),
        },
        {
          hid: "og:image",
          name: "og:image",
          content: this.game_data.cover_url_big,
        },
      ],
    };
  },
};
</script>