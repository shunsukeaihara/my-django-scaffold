const createState = () => ({
  menuVisible: true,
  footerVisible: true,
})

const getters = {
  menuVisible: ({ menuVisible }) => menuVisible,
  footerVisible: ({ footerVisible }) => footerVisible
}

const actions = {
  setMenuVisible: ({ commit, state }, value) => {
    if (state.menuVisible !== Boolean(value)) commit('SET_MENU_VISIBLE', value)
  },
  showMenu: ({ commit }) => commit('SET_MENU_VISIBLE', true),
  hideMenu: ({ commit }) => commit('SET_MENU_VISIBLE', false),
  toggleMenu: ({ commit }) => commit('TOGGLE_MENU'),
  setFooterVisibility: ({ commit }, value) => commit('SET_FOOTER_VISIBLE', value),
}

const mutations = {
  SET_MENU_VISIBLE(state, value) {
    state.menuVisible = Boolean(value)
  },
  TOGGLE_MENU(state) {
    state.menuVisible = !state.menuVisible
  },
  SET_FOOTER_VISIBLE(state, value) {
    state.footerVisible = Boolean(value)
  },
  SET(state, obj) {
    Object.keys(obj).forEach(k => { state[k] = obj[k] })
  },
}

export default {
  state: createState,
  namespaced: true,
  getters,
  actions,
  mutations,
}