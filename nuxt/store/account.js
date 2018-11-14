export const TOKEN_COOKIE_NAME = 'jwttoken'

const createState = () => ({
  user: null,
  token: null
})

const mutations = {
  LOGOUT(state) {
    Object.assign(state, createState())
    this.app.$cookie.remove(TOKEN_COOKIE_NAME)
    this.$router.push({ name: 'login' })
  },
  LOGIN(state, { token, user }) {
    state.token = token
    this.app.$cookie.set(TOKEN_COOKIE_NAME, token)
    state.user = user
  }
}

const actions = {
  setUserInfo({ commit }, { token, user }) {
    return commit("LOGIN", { token: token, user: user })
  },
  login({ commit }, data) {
    return this.$http.auth.login(data)
      .then(res => commit("LOGIN", res.data))
      .catch(() => commit("LOGOUT"))
  },
  refresh({ commit }) {
    let token = this.app.$cookie.get(TOKEN_COOKIE_NAME)
    if (token) {
      return this.$http.auth.refresh({ token: token })
        .then(res => commit("LOGIN", res.data))
        .catch(() => commit("LOGOUT"))
    }
  },
  logout({ commit }) {
    commit("LOGOUT")
  }
}

const getters = {
  token: ({ token }) => {
    return token
  },
  user: ({ user }) => {
    return user
  },
  isLoggedIn: ({ token }) => {
    return token ? true : false
  }
}

export default {
  state: createState,
  namespaced: true,
  getters,
  actions,
  mutations,
}