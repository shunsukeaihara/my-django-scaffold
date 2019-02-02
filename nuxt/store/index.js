import Vuex from 'vuex'
import cookie from 'js-cookie'
import screen from './screen'
import account, { TOKEN_COOKIE_NAME } from './account'
import tokenInfo from './tokenInfo'

function createPersistentPlugin(module) {
  let re = new RegExp(`^${module}/`)
  return store => {
    store.subscribe((mutation, state) => {
      //console.log('subscribe', mutation, JSON.stringify(state[module]), mutation.type.match(re))
      if (mutation.type.match(re)) {
        store.app.$cookie.setJson(`store-${module}`, state[module])
      }
    })
  }
}

export default () => {
  let store = new Vuex.Store({
    actions: {
      async nuxtServerInit({ dispatch, commit }, { req, app: { $cookie } }) {
        let token = $cookie.get(TOKEN_COOKIE_NAME)
        if (token) {
          await dispatch('account/refresh')
        }
        let screenInfo = req.cookies['store-screen']
        if (screenInfo) await commit('screen/SET', JSON.parse(screenInfo))
        let storedTokenInfo = req.cookies['store-tokenInfo']
        if (storedTokenInfo) await commit('tokenInfo/SET', JSON.parse(storedTokenInfo))
        return Promise.resolve()
      },
      async nuxtClientInit({ dispatch }, { app: { $cookie } }) {
        let token = $cookie.get(TOKEN_COOKIE_NAME)
        if (token) {
          return dispatch('account/refresh')
        }
      }
    },
    modules: {
      account,
      screen,
      tokenInfo,
    },
    plugins: [createPersistentPlugin('screen'), createPersistentPlugin('tokenInfo')],
  })
  if (process.browser) {
    // spaでの初期化の場合はnuxtClientInitではなくここでやらないと間に合わない
    let token = cookie.get(TOKEN_COOKIE_NAME)
    if (token) {
      store.state.account.token = token
    }
    let screenInfo = cookie.get('store-screen')
    if (screenInfo) screen.mutations.SET(store.state.screen, JSON.parse(screenInfo))
  }

  return store
}