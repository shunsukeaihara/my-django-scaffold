import * as utils from '@/utils'
import Vue from 'vue'
import CheckboxIcon from '@/components/CheckboxIcon'
Vue.component('CheckboxIcon', CheckboxIcon)

export default (context, inject) => {
  inject('e', utils.errProp)

  inject('createHttpErrorHandler', utils.createHttp400ErrorHandler)
  inject('createErrorDict', utils.initialErrorDict)
}