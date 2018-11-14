import Vue from 'vue'
import Vuex from 'vuex'
import cookie from 'js-cookie'
import screen from './screen'
import account from './account'
Vue.use(Vuex)

// cookieにstateを保存するplugin
function createPersistentPlugin(module) {
  let re = new RegExp(`^${module}/`)
  return store => {
    store.subscribe((mutation, state) => {
      // console.log('subscribe', mutation, JSON.stringify(state[module]), mutation.type.match(re))
      if (mutation.type.match(re)) {
        cookie.set(`store-${module}`, state[module])
      }
    })
  }
}

export default new Vuex.Store({
  modules: {
    screen: screen,
    account: account,
  },
  plugins: [createPersistentPlugin('screen')],
})