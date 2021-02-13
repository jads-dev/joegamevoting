<template>
  <v-app dark style="min-width: 1200px">
    <v-app-bar fixed app>
      <v-btn to="/"> Home </v-btn>

      <v-switch hide-details v-model="official" label="Show Official Discord votes" class="ml-2" @change="on_official_change"> </v-switch>

      <div v-if="official" class="d-flex flex-column ml-2">
        <audio style="width: 400px; height: 15px" controls loop>
          <source src="https://cdn.discordapp.com/attachments/666328917237563419/809882988137414666/Voting_Theme_Loop.mp3" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
        Voting theme by tieff (WIP).
      </div>
      <template v-if="!official">
        <v-spacer />
        <game-search-bar />
      </template>

      <v-spacer />
      <template v-if="user.username">
        <v-chip pill class="mr-1">
          <v-avatar left>
            <v-img :src="user.avatar_url" :alt="user.username"></v-img>
          </v-avatar>
          {{ user.username }}
        </v-chip>
        <v-btn small @click="logout()"> Logout </v-btn>
      </template>
      <v-btn v-else color="#7289DA" href="/api/login">
        <img style="max-width: 25px; max-height: 25px" src="https://discord.com/assets/1c8a54f25d101bdc607cec7228247a9a.svg" />
        Login with discord
      </v-btn>
    </v-app-bar>
    <v-main style="height: 100vh">
      <v-row style="height: 100%" no-gutters>
        <v-col cols="6" sm="3" :md="calc_wideness_left()" style="height: 100%; scrollbar-width: thin" class="overflow-y-auto">
          <game-votes-discord v-if="official" class="ma-0 pa-0" />
          <game-votes v-else class="ma-0 pa-0" />
        </v-col>
        <v-col cols="6" sm="9" :md="calc_wideness_right()" style="height: 100%" class="overflow-y-auto pl-2 pr-3">
          <nuxt />
        </v-col>
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
import GameSearchBar from "../components/GameSearchBar.vue";
import GameVotes from "../components/GameVotes.vue";
import GameVotesDiscord from "../components/GameVotesDiscord.vue";
export default {
  components: { GameSearchBar, GameVotes, GameVotesDiscord },
  created: async function () {
    const token = this.$store.state.localStorage.user.token;
    const username = this.$store.state.localStorage.user.username;
    if (token) {
      this.$axios.setToken(token, "Bearer");
      if (!username) {
        const response = await this.$axios.$get("/api/me");
        const user = {
          username: response["username"],
          avatar_url: response["avatar_url"],
          can_vote: response["can_vote"],
        };
        this.$store.commit("localStorage/set_user", user);
      }
    }
  },

  data() {
    return {};
  },

  methods: {
    logout() {
      this.$store.commit("localStorage/reset_state", !this.adding_event);
    },
    on_official_change() {
      this.$router.push({
        path: "/",
      });
    },
    calc_wideness_left() {
      if (this.wide_mode) {
        if (this.show_hells) return "6";
        else return "4";
      } else {
        if (this.show_hells) return "4";
        else return "2";
      }
    },
    calc_wideness_right() {
      if (this.wide_mode) {
        if (this.show_hells) return "6";
        else return "8";
      } else {
        if (this.show_hells) return "8";
        else return "10";
      }
    },
  },
  computed: {
    user: {
      get() {
        return this.$store.state.localStorage.user;
      },
      set(value) {},
    },
    official: {
      get() {
        return this.$store.state.localStorage.official;
      },
      set(value) {
        this.$store.commit("localStorage/set_official", value);
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
    show_hells: {
      get() {
        return this.$store.state.localStorage.show_hells;
      },
      set(value) {
        this.$store.commit("localStorage/set_show_hells", value);
      },
    },
  },
};
</script>


<style>
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #424242;
}

::-webkit-scrollbar-thumb {
  background: #757575;
}

::-webkit-scrollbar-thumb:hover {
  background: #bdbdbd;
}

html {
  overflow-y: hidden !important;
  overflow-x: auto;
}
</style>