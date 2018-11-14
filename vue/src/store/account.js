import cookie from 'js-cookie'
export const TOKEN_COOKIE_NAME = 'jwttoken'

const createState = () => ({
  user: null,
  token: null
})

const mutations = {
  LOGOUT(state) {
    Object.assign(state, createState())
    cookie.remove(TOKEN_COOKIE_NAME)
    this.$router.push({ name: 'login' })
  },
  LOGIN(state, { token, user }) {
    state.token = token
    cookie.set(TOKEN_COOKIE_NAME, token)
    state.user = user
  }
}

const actions = {
  setUserInfo(context, { token, user }) {
    context.commit("LOGIN", { token: token, user: user })
  },
  login(context, data) {
    return this.$http.auth().login(data).then(res => {
      context.commit("LOGIN", res.data)
    }, () => context.commit("LOGOUT"))
  },
  refresh(context, data) {
    return this.$http.auth().refresh(data).then(res => {
      context.commit("LOGIN", res.data)
    }, () => context.commit("LOGOUT"))
  },
  logout(context) {
    context.commit("LOGOUT")
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