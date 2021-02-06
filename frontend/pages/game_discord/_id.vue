<template>
  <div>
    <v-card>
      <v-row no-gutters>
        <v-col cols="12" md="2">
          <v-img width="300px" :src="game_data.cover_url_big"></v-img>
        </v-col>
        <v-col cols="12" md="10">
          <v-card-title class="text-h3">
            <span>{{ selected_game.name }}</span>
          </v-card-title>
          <v-card-subtitle class="mb-0 pb-0">
            <span class="text-overline"> {{ game_data.release_date | date }} <br /> </span>
            <span class="text-overline">
              {{ game_platforms.join(", ") }}
            </span>
          </v-card-subtitle>
          <v-card-subtitle>
            <v-btn color="#7289da" :href="`https://discord.com/channels/308515582817468420/807289103920922684/${this.$route.params.id}`" target="_blank"
              >Discord Message
            </v-btn>
          </v-card-subtitle>
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
                <v-img :src="'//cdn.discordapp.com' + voter.avatar_url" :alt="voter.name"></v-img>
              </v-avatar>
              {{ voter.name }}
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
    game_pitches: [],
    game_voters: [],
    pitch: "",
  }),
  created: async function () {
    this.$store.commit("localStorage/set_official", true);
    const game_data = await this.$axios.$get(`/api/game_discord/${this.$route.params.id}`);
    this.game_data = game_data;

    const game_platforms = await this.$axios.$get(`/api/game_discord/platforms/${this.$route.params.id}`);
    this.game_platforms = game_platforms.map(function (obj) {
      return obj.name;
    });

    const game_voters = await this.$axios.$get(`/api/game_discord/${this.$route.params.id}/voters`);
    this.game_voters = game_voters;

    const game_pitches = await this.$axios.$get(`/api/game_discord/${this.$route.params.id}/pitches`);
    this.game_pitches = game_pitches;
  },

  methods: {
    pitch_game: async function () {
      var params = {
        pitch: this.pitch,
      };
      await this.$axios.$post(`/api/game_discord/${this.$route.params.id}/pitch`, params);

      const game_pitches = await this.$axios.$get(`/api/game_discord/${this.$route.params.id}/pitches`);
      this.game_pitches = game_pitches;

      const game_data = await this.$axios.$get(`/api/game_discord/${this.$route.params.id}`);
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
    games: {
      get() {
        return this.$store.state.discord_games;
      },
      set(value) {},
    },
    selected_game: {
      get() {
        for (const game in this.games) {
          if (this.games[game].message_id == this.$route.params.id) return this.games[game];
        }
        return {};
      },
      set(value) {},
    },
  },

  asyncData(context) {
    return context.$axios.get(`/api/game_discord/${context.route.params.id}`).then((res) => {
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