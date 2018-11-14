import Vue from 'vue'
import Router from 'vue-router'
import store from './store'

import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [{
      path: '/login',
      name: 'login',
      component: () =>
        import('./views/Login.vue'),
      meta: { publicAvailable: true },
      beforeEnter: (to, from, next) => {
        if (store.getters['account/isLoggedIn']) {
          next(to.query.redirect ? to.query.redirect : "/")
        }
        next()
      }
    },
    {
      path: '/',
      name: 'home',
      component: Home
    }
  ]
})