import cookie from 'js-cookie'
import Vue from 'vue'
import App from './App.vue'
import './plugins/vuetify'
import './plugins/form'
import router from './router'
import store from './store'
import { TOKEN_COOKIE_NAME } from './store/account'
import createHttpClient from './http'

Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  // ログイン済みでない場合にpublicではないページにアクセスした場合はloginに飛ばす
  if (!to.matched.every(record => record.meta.publicAvailable)) {
    // 名前ベースのアクセス微妙だけど仕方ない
    if (!store.getters['account/isLoggedIn']) {
      next({ name: "login", query: { redirect: to.fullPath } });
    }
  }
  next();
})



let http = createHttpClient(store)
Vue.prototype.$http = http
store.$http = http
store.$router = router


// initialize store ちょいダサい
// nuxtならinitialize hookがある
let token = cookie.get(TOKEN_COOKIE_NAME)
if (token) {
  store.state.account.token = token
  store.dispatch("account/refresh", { token: token })
}
let storedScreen = cookie.get('store-screen')
if (storedScreen) store.commit('screen/SET', JSON.parse(storedScreen))

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')