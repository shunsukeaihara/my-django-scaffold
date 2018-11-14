import Vue from 'vue'
import MyInput from '@/components/form/MyInput'
import MySelect from '@/components/form/MySelect'
import MyCheckbox from '@/components/form/MyCheckbox'
import MyDateInput from '@/components/form/MyDateInput'
import NonFieldErrors from '@/components/form/NonFieldErrors'

Vue.component('MyInput', MyInput)
Vue.component('MySelect', MySelect)
Vue.component('MyCheckbox', MyCheckbox)
Vue.component('MyDateInput', MyDateInput)
Vue.component('NonFieldErrors', NonFieldErrors)

export function createErrorDict(form) {
  let r = { nonFieldErrors: [] }
  Object.keys(form).forEach(k => { r[k] = [] })
  return r
}

export function clearErrorDict(errDict) {
  Object.keys(errDict).forEach(k => { errDict[k] = [] })
}

export function handleHttpError(err, errorDict) {
  // TODO: 401のtokenのexpireに対応
  clearErrorDict(errorDict)
  let response = err.response
  if (response) {
    if (response.status === 400) {
      let data = response.body || response.data
      Object.keys(data).forEach(k => { errorDict[k] = data[k] })
    }
  } else {
    console.log(err, response)
    errorDict.nonFieldErrors.push('予期しないエラーが発生しました。')
    return err
  }
}

function install(Vue, opts) {
  opts = Object.assign({
    name: 'form',
    formProp: 'form',
    errorProp: 'errors',
  }, opts || {})
  let name = '$' + opts.name
  if (Vue.prototype[name]) {
    delete Vue.prototype[name]
  }
  Object.defineProperty(Vue.prototype, name, {
    configurable: true,
    get() {
      var self = this
      let cached = self._$form
      // NOTE: 開発中にautoreloadが走るとvmが
      if (cached && cached.vm === self) return self._$form
      let r = {
        vm: self,
        init() {
          let form = self.$data[opts.formProp]
          self.$data[opts.errorProp] = createErrorDict(form)
        },
        clearError() {
          clearErrorDict(self.$data[opts.errorProp])
        },
        handleError(err) {
          return handleHttpError(err, self.$data[opts.errorProp])
        },
      }
      this._$form = r
      return r
    },
  })

  Object.defineProperty(Vue.prototype, '$_form', {
    configurable: true,
    get() {
      return {
        createErrorDict,
        clearErrorDict,
        handleError(e, errDict) {
          handleHttpError(e, errDict)
          return errDict
        },
      }
    },
  })
}
Vue.use(install)