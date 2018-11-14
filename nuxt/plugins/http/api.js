import axiosBase from 'axios'
import qs from 'qs'

import changePropCase from '@/misc/change-prop-case'

function toSnake(data) { return changePropCase.snake(data) }

function setErrorStatus(error) {
  if (error.response) {
    error.status = error.statusCode = error.response.status
  }
  return Promise.reject(error)
}

/*
function all(paramsOrCb, cb) {
  let params = paramsOrCb
  if (typeof paramsOrCb === 'function') {
    cb = paramsOrCb
    params = {}
  } else {
    params = params || {}
  }

  let r = []
  let request = offset => {
    params = Object.assign({}, params, { offset })
    return this.list(params).then(res => {
      r = r.concat(res.data.results)
      if (typeof cb === 'function') cb(r, res, offset)
      if (res.data.next) return request(r.length)
      else return r
    })
  }
  return request(0)
}
*/

function createAxiosInstance(baseURL, store, req) {
  let headers = { common: {} }

  if (process.server) {
    // NOTE: サーバ側のAPIリクエストはnginxを経由しないため
    // nginxのproxy_set_headerで設定する項目をここで設定する
    const url = require('url')
    const endpointUrl = url.parse(process.env.NUXT_ENV_API_ENDPOINT)
    headers.common['Host'] = endpointUrl.host
    headers.common['X-Forwarded-Proto'] = endpointUrl.protocol
    headers.common['X-Forwarded-For'] = req.headers['x-forwarded-for'] || ''
  }

  let axiosInstance = axiosBase.create({
    paramsSerializer: (params) => qs.stringify(toSnake(params), { indices: false }),
    headers: headers,
    baseURL,
  })

  // set token interceptors
  axiosInstance.interceptors.response.use(res => res, setErrorStatus)
  axiosInstance.interceptors.request.use(config => {
    // NOTE: axios.defaultsを使用すると別ユーザに影響がでるため
    // interceptorでtokenをセットする
    let token = store.state.account.token
    if (token) config.headers.common['Authorization'] = 'JWT ' + token
    return config
  }, err => Promise.reject(err))

  // NOTE: asyncDataで401が発生した場合はerrorページに飛ぶが、axios.post等で401が発生するかもしれない
  // googleっぽく再度ログインが必要な旨を表示するモーダルを出すようにすべきかもしれない
  axiosInstance.interceptors.response.use(res => res, error => {
    let response = error.response
    if (response && response.status === 401) {
      console.log('axios interceptor reponse: data', response.data)
      if (response.data && response.data.detail === 'Signature has expired.') {
        store.commit('account/LOGOUT')
      }
    }
    return Promise.reject(error)
  })
  return axiosInstance
}

export default function(env, store, req) {
  let apiEndpoint = process.server ? process.env.PRIVATE_API_ENDPOINT : env.NUXT_ENV_API_ENDPOINT
  let api = createAxiosInstance(apiEndpoint, store, req)
  return {
    axios: axiosBase,
    axiosInstance: api,
    toSnake,
    auth: {
      login: data => api.post('/v1/auth/login/', data),
      refresh: data => api.post('v1/auth/refresh/', data),
    },
  }
}