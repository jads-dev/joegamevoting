export const state = () => ({
  discord_games: {}
});

export const mutations = {
  set_discord_games(state, games) {
    state.discord_games = games;
  }
};
