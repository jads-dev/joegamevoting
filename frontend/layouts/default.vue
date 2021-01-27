<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-btn to="/"> Home </v-btn>
      <v-spacer />

      <game-search-bar />

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
    <v-main>
      <v-row class="mr-2 mt-2" no-gutters>
        <v-col cols="2">
          <game-votes />
        </v-col>
        <v-col cols="10">
          <nuxt />
        </v-col>
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
import GameSearchBar from "../components/GameSearchBar.vue";
import GameVotes from "../components/GameVotes.vue";
export default {
  components: { GameSearchBar, GameVotes },
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
    return {
      loginurl: "",
    };
  },

  methods: {
    logout() {
      this.$store.commit("localStorage/reset_state", !this.adding_event);
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
  overflow-y: auto !important;
}
</style>