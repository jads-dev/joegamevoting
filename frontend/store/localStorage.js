export const state = () => ({
  user: {
    token: "",
    username: "",
    avatar_url: "",
    can_vote: false
  }
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
  }
};
