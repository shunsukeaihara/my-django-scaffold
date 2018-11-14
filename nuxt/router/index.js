import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

function hook(m) {
  return m.default || m
}

function scrollBehavior(to, from, savedPosition) {
  // 返された位置が偽または空のオブジェクトだったときは、
  // 現在のスクロール位置を保持する
  let position = false

  // 子パスが見つからないとき
  if (to.matched.length < 2) {
    // ページのトップへスクロールする
    position = { x: 0, y: 0 }
  } else if (to.matched.some((r) => r.components.default.options.scrollToTop)) {
    // 子パスのひとつが scrollToTop オプションが true にセットされているとき
    position = { x: 0, y: 0 }
  }

  // savedPosition は popState ナビゲーションでのみ利用できます（戻るボタン）
  if (savedPosition) {
    position = savedPosition
  }

  return new Promise(resolve => {
    //（必要であれば）out トランジションが完了するのを待つ
    window.$nuxt.$once('triggerScroll', () => {
      // セレクタが渡されなかったとき、
      // または、セレクタがどの要素にもマッチしなかったときは、座標が用いられる
      if (to.hash && document.querySelector(to.hash)) {
        // セレクタを返すことでアンカーまでスクロールする
        position = { selector: to.hash }
      }
      resolve(position)
    })
  })
}


export function createRouter() {
  return new Router({
    mode: 'history',
    scrollBehavior,
    routes: [{
        name: 'index',
        path: '/',
        component: () => import('~/views/index.vue').then(hook),
      },
      {
        name: 'login',
        path: '/login',
        component: () => import('~/views/login.vue').then(hook),
      },
      {
        name: 'home',
        path: '/home',
        component: () => import('~/views/home.vue').then(hook),
        meta: { requiresAuth: true },
      },
    ]
  })
}