// requierd: js-cookie, cookies, moment
import moment from 'moment'

class CookieWrap {
  constructor(cookie) {
    this._cookie = cookie
    this.options = {
      secure: false,
      domain: null,
      httpOnly: false,
    }
  }

  mergeOptions(obj) { return Object.assign(obj, this.options) }

  get(key) { return this._cookie.get(key, this.options) }

  set(key, value) {
    if (process.server) {
      this._cookie.set(key, value, this.mergeOptions({ expires: moment().add(7, 'days').toDate() }))
    } else {
      this._cookie.set(key, value, this.mergeOptions({ expires: 7 }))
    }
  }

  remove(key) {
    if (process.server) {
      this._cookie.set(key, '', this.mergeOptions({ expires: new Date(0) }))
    } else {
      this._cookie.remove(key, this.options)
    }
  }
}

export default ({ req, res }, inject) => {
  let cookieInterface
  if (process.server) {
    const Cookies = require('cookies')
    cookieInterface = new Cookies(req, res, { secure: true })
  } else {
    cookieInterface = require('js-cookie')
  }
  inject('cookie', new CookieWrap(cookieInterface))
}