export const TOKEN_INFO_KEY = 'store-tokenInfo'


const createState = () => ({
  activate: {},
  emailChange: {},
  passwordReset: {},
})

const mutations = {
  RESET(state) {
    Object.assign(state, createState())
    //this.app.$cookie.setJson(TOKEN_INFO_KEY, state)
  },
  SET(state, obj) {
    Object.keys(obj).forEach(k => { state[k] = obj[k] })
    //this.app.$cookie.setJson(TOKEN_INFO_KEY, state)
  },
  SET_ACTIVATE_INFO(state, { token, email, error }) {
    Object.assign(state, createState())
    state.activate = { token: token, email: email, error: error }
    //this.app.$cookie.setJson(TOKEN_INFO_KEY, state)
  },
  SET_PASSWORD_RESET_INFO(state, { token, email, error }) {
    Object.assign(state, createState())
    state.passwordReset = { token: token, email: email, error: error }
    //this.app.$cookie.setJson(TOKEN_INFO_KEY, state)
  },
  SET_EMAIL_CHANGE_INFO(state, { token, email, error }) {
    Object.assign(state, createState())
    state.emailChange = { token: token, email: email, error: error }
    //this.app.$cookie.setJson(TOKEN_INFO_KEY, state)
  },
}

const actions = {
  resetTokenInfo({ commit }) {
    return commit("RESET")
  },
  setActivateInfo({ commit }, data) {
    return commit("SET_ACTIVATE_INFO", data)
  },
  setPasswordResetInfo({ commit }, data) {
    return commit("SET_PASSWORD_RESET_INFO", data)
  },
  setEmailChangeInfo({ commit }, data) {
    return commit("SET_EMAIL_CHANGE_INFO", data)
  },
  persist({ commit }, data) {
    return commit("PERSIST", data)
  }
}

const getters = {
  activateInfo: ({ activate }) => {
    return activate
  },
  passwordResetInfo: ({ passwordReset }) => {
    return passwordReset
  },
  emailChangeInfo: ({ emailChange }) => {
    return emailChange
  }
}

export default {
  state: createState,
  namespaced: true,
  getters,
  actions,
  mutations,
}