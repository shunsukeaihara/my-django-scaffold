import * as utils from '@/utils'

export default (context, inject) => {
  inject('e', utils.errProp)

  inject('createHttpErrorHandler', utils.createHttp400ErrorHandler)
  inject('createErrorDict', utils.initialErrorDict)
}