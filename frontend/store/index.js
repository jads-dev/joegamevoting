export const state = () => ({
  discord_games: {},
  latest_pitches: [],
  random_pitches: []
});

export const mutations = {
  set_discord_games(state, games) {
    state.discord_games = games;
  },
  set_latest_pitches(state, pitches) {
    state.latest_pitches = pitches;
  },
  set_random_pitches(state, pitches) {
    state.random_pitches = pitches;
  }
};
