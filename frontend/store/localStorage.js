export const state = () => ({
  user: {
    token: "",
    username: "",
    avatar_url: "",
    can_vote: false
  },
  official: true,
  dark_mode: true,
  show_weeb_status: true
});

export const mutations = {
  set_token(state, token) {
    state.user.token = token;
  },
  set_user(state, user) {
    state.user.username = user.username;
    state.user.avatar_url = user.avatar_url;
    state.user.can_vote = user.can_vote;
  },
  reset_state(state) {
    state.user = {
      token: "",
      username: "",
      avatar_url: "",
      can_vote: false
    };
  },
  set_official(state, official) {
    state.official = official;
  },
  set_dark_mode(state, dark_mode) {
    state.dark_mode = dark_mode;
  },
  set_show_weeb_status(state, value) {
    state.show_weeb_status = value;
  }
};
