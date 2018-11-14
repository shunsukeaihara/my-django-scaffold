export default function({ store, route, redirect }) {
  if (route.matched.some(record => record.meta.requiresAuth)) {
    let isLoggedIn = store.getters['account/isLoggedIn']
    if (!isLoggedIn) {
      redirect('/login', {
        next: route.fullPath,
      })
    }
  }
}