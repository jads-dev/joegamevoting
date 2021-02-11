<template>
  <v-row>
    <v-col cols="12">
      <v-slider label="Day" :min="day_min" :max="day_max" v-model="selected_day"></v-slider>
    </v-col>
    <v-col cols="12">
      <v-slider label="Hour" :min="hour_min" :max="hour_max" v-model="selected_hour"></v-slider>
    </v-col>
    <v-col cols="12">
      <v-slider label="Minute" :min="minute_min" :max="minute_max" v-model="selected_minute"></v-slider>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    day_min: 0,
    day_max: 0,
    hour_min: 0,
    hour_max: 0,
    minute_min: 0,
    minute_max: 0,
    dates: [],
    selected_day: 0,
    selected_hour: 0,
    selected_minute: 0,
  }),

  mounted: async function () {
    // this.$store.commit("localStorage/set_official", false);
    console.log("asx");
    const files = await this.$axios.$get(`/api/game_discord/vote_files/`);
    var max_date = new Date(Math.max(...files.map((e) => new Date(e.date))));
    console.log(max_date);
  },

  methods: {
    get_hour_max: function () {
      this.$router.push({
        path: "/game_discord/" + game.message_id,
      });
    },
  },
};
</script>