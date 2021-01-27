<template>
  <div>
    {{ user }}
  </div>
</template>


<script>
export default {
  mounted: async function () {
    const token = this.$store.state.localStorage.user.token;
    this.$axios.setToken(token, "Bearer");
    const response = await this.$axios.$get("/api/me");
    this.user = response;
  },
  data: () => ({
    user: {},
  }),
};
</script>