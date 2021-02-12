export { default as GameSearchBar } from '../..\\components\\GameSearchBar.vue'
export { default as GameVotes } from '../..\\components\\GameVotes.vue'
export { default as GameVotesDiscord } from '../..\\components\\GameVotesDiscord.vue'
export { default as VoteList } from '../..\\components\\VoteList.vue'
export { default as VoteListSimple } from '../..\\components\\VoteListSimple.vue'

export const LazyGameSearchBar = import('../..\\components\\GameSearchBar.vue' /* webpackChunkName: "components/game-search-bar" */).then(c => c.default || c)
export const LazyGameVotes = import('../..\\components\\GameVotes.vue' /* webpackChunkName: "components/game-votes" */).then(c => c.default || c)
export const LazyGameVotesDiscord = import('../..\\components\\GameVotesDiscord.vue' /* webpackChunkName: "components/game-votes-discord" */).then(c => c.default || c)
export const LazyVoteList = import('../..\\components\\VoteList.vue' /* webpackChunkName: "components/vote-list" */).then(c => c.default || c)
export const LazyVoteListSimple = import('../..\\components\\VoteListSimple.vue' /* webpackChunkName: "components/vote-list-simple" */).then(c => c.default || c)
