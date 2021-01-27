<template>
  <div>
    {{ message }}
  </div>
</template>

<script>
export default {
  mounted: async function () {
    const code = this.$route.query.code;
    const state = this.$route.query.state;

    var response = await this.$axios.$get(`/api/discord_callback?code=${code}&state=${state}`);

    this.$axios.setToken(response["access_token"], "Bearer");
    this.$store.commit("localStorage/set_token", response["access_token"]);

    this.message = "Sending user back to homepage.";

    window.location.href = "/";

    response = await this.$axios.$get("/api/me");

    const user = {
      username: response["username"],
      avatar_url: response["avatar_url"],
      can_vote: response["can_vote"],
    };

    this.$store.commit("localStorage/set_user", user);
  },

  data: () => ({
    message: "",
  }),
};
</script>