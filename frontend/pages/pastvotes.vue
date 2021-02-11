<template>
  <v-row>
    <v-col cols="12">
      <div>File:</div>

      <select v-model="selected" style="color: white" size="30" @change="on_file_change">
        <option v-for="file in files" :value="file" :key="file">{{ file }}</option>
      </select>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    files: {},
    selected: "",
    vote_data: {},
  }),

  mounted: async function () {
    const files = await this.$axios.$get(`/api/game_discord/vote_files/`);
    this.files = files;
  },

  methods: {
    on_file_change: async function () {
      const vote_data = await this.$axios.$get(`/api/game_discord/vote_file/${this.selected}`);
      this.vote_data = vote_data;
      this.$store.commit("set_historical_votes", vote_data);
    },
  },
};
</script>
