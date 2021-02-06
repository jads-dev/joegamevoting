export const state = () => ({
  discord_games: {},
  latest_pitches: []
});

export const mutations = {
  set_discord_games(state, games) {
    state.discord_games = games;
  },
  set_latest_pitches(state, pitches) {
    state.latest_pitches = pitches;
  }
};
