import Vue from 'vue'
import Router from 'vue-router'
import { normalizeURL, decode } from '@nuxt/ufo'
import { interopDefault } from './utils'
import scrollBehavior from './router.scrollBehavior.js'

const _55d8fe67 = () => interopDefault(import('..\\pages\\discord_callback.vue' /* webpackChunkName: "pages/discord_callback" */))
const _ddc3eb72 = () => interopDefault(import('..\\pages\\me.vue' /* webpackChunkName: "pages/me" */))
const _6051b318 = () => interopDefault(import('..\\pages\\pastvotes.vue' /* webpackChunkName: "pages/pastvotes" */))
const _0e6f0a81 = () => interopDefault(import('..\\pages\\test.vue' /* webpackChunkName: "pages/test" */))
const _066bbc48 = () => interopDefault(import('..\\pages\\game_discord\\_id.vue' /* webpackChunkName: "pages/game_discord/_id" */))
const _1a803229 = () => interopDefault(import('..\\pages\\game\\_id.vue' /* webpackChunkName: "pages/game/_id" */))
const _4f6ffe1a = () => interopDefault(import('..\\pages\\index.vue' /* webpackChunkName: "pages/index" */))

// TODO: remove in Nuxt 3
const emptyFn = () => {}
const originalPush = Router.prototype.push
Router.prototype.push = function push (location, onComplete = emptyFn, onAbort) {
  return originalPush.call(this, location, onComplete, onAbort)
}

Vue.use(Router)

export const routerOptions = {
  mode: 'history',
  base: '/',
  linkActiveClass: 'nuxt-link-active',
  linkExactActiveClass: 'nuxt-link-exact-active',
  scrollBehavior,

  routes: [{
    path: "/discord_callback",
    component: _55d8fe67,
    name: "discord_callback"
  }, {
    path: "/me",
    component: _ddc3eb72,
    name: "me"
  }, {
    path: "/pastvotes",
    component: _6051b318,
    name: "pastvotes"
  }, {
    path: "/test",
    component: _0e6f0a81,
    name: "test"
  }, {
    path: "/game_discord/:id?",
    component: _066bbc48,
    name: "game_discord-id"
  }, {
    path: "/game/:id?",
    component: _1a803229,
    name: "game-id"
  }, {
    path: "/",
    component: _4f6ffe1a,
    name: "index"
  }],

  fallback: false
}

function decodeObj(obj) {
  for (const key in obj) {
    if (typeof obj[key] === 'string') {
      obj[key] = decode(obj[key])
    }
  }
}

export function createRouter () {
  const router = new Router(routerOptions)

  const resolve = router.resolve.bind(router)
  router.resolve = (to, current, append) => {
    if (typeof to === 'string') {
      to = normalizeURL(to)
    }
    const r = resolve(to, current, append)
    if (r && r.resolved && r.resolved.query) {
      decodeObj(r.resolved.query)
    }
    return r
  }

  return router
}
