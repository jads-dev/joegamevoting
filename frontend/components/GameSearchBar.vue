<template>
  <v-autocomplete
    ref="card_autocomplete"
    v-model="selected_game"
    :items="search_games"
    :loading="is_searching"
    :search-input.sync="search_query"
    hide-details
    hide-no-data
    dense
    item-text="name"
    item-value="id"
    label="Search Games"
    placeholder="Start typing to search"
    prepend-icon="mdi-magnify"
    return-object
    :filter="filter_search"
    auto-select-first
    v-on:keyup.enter="on_game_select"
    @change="on_game_select"
    style="max-width: 500px"
  >
    <template v-slot:item="{ item }">
      <v-img class="mr-2" max-height="50" max-width="50" :src="item.cover_url"></v-img>
      <v-list-item-content>
        <v-list-item-title v-text="item.name"></v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script>
function escapeRegExp(string) {
  return string.replace(/[.*+\-?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
}

export default {
  data: () => ({
    selected_game: null,
    search_query: null,
    search_games: [],
    is_searching: false,
  }),

  watch: {
    search_query(val) {
      this.fetch_games(val);
    },
  },

  methods: {
    async fetch_games(val) {
      var params = {
        search_term: val,
      };
      if (val) {
        this.is_searching = true;
        var result = await this.$axios.$get("/api/game/search", {
          params: params,
        });
        this.search_games = result;
        this.is_searching = false;
      } else {
        this.search_games = [];
      }
    },
    filter_search(item, queryText, itemText) {
      return true;
    },
    on_game_select() {
      window.location.href = "/game/" + this.selected_game.id;
    },
  },
};
</script>