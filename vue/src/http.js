import axiosBase from 'axios'

function createAxiosInstance(store) {
  axiosBase.defaults.baseURL = process.env.VUE_APP_API_ENDPOINT
  let axiosInstance = axiosBase.create()
  axiosInstance.interceptors.request.use(config => {
    let token = store.getters.token
    if (token) config.headers.common['Authorization'] = 'JWT ' + token
    return config
  }, err => Promise.reject(err))
  axiosInstance.interceptors.response.use(res => res, error => {
    let response = error.response
    if (response && response.status === 401) {
      store.commit('LOGOUT')
    }
    return Promise.reject(error)
  })
  return axiosInstance
}

export default function(store) {
  let axios = createAxiosInstance(store)
  return {
    auth: () => ({
      login: (data) => axios.post('/v1/auth/login/', data),
      refresh: (data) => axios.post('/v1/auth/refresh/', data)
    })
  }
}