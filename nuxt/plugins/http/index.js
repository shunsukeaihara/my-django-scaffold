import createAPI from './api'

function errToProps(err) {
  let res = err.response
  if (res) {
    if (res.data) console.error('errToProps ($e):', res.headers, res.data)
    console.error(res.status, res.statusText)
    return {
      status: res.status,
      statusCode: res.status,
      message: res.statusText,
    }
  } else {
    console.warn('errToProps ($e):', err)
    return {
      status: 500,
      statusCode: 500,
      message: 'Internal Server Error',
    }
  }
}

// required nuxt-env.
export default ({ app: { $env }, store, req }, inject) => {
  let api = createAPI($env, store, req)
  inject('http', api)
  inject('e', errToProps)
  store.$http = api
}