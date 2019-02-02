export function createHttp400ErrorHandler(errorDict) {
  clearErrors(errorDict)
  return err => {
    let res = err.response
    if (!res) throw err
    if (res.status === 400) {
      let data = res.data
      Object.keys(data).forEach(k => {
        errorDict[k] = data[k]
      })
    } else {
      errorDict.nonFieldErrors = [`${res.status} ${res.statusText}`]
    }
  }
}
export function clearErrors(errorDict) {
  Object.keys(errorDict).forEach(k => {
    errorDict[k] = []
  })
}
export function initialErrorDict(form) {
  let r = { nonFieldErrors: [] }
  Object.keys(form).forEach(k => { r[k] = [] })
  return r
}

export function errProp(err) {
  let res = err.response
  // console.error(err)
  if (res) {
    // if (res.data) console.error(res.data)
    return {
      status: res.status,
      statusCode: res.status,
      message: res.statusText,
    }
  } else {
    //console.error('errToProps ($e):', err)
    return {
      status: 500,
      statusCode: 500,
      message: 'Internal Server Error',
    }
  }
}

// 配列のformのエラーを生成するのに使う
export function zipFormError(array, errors) {
  let r = []
  for (let i = 0; i < array.length; ++i) {
    let form = array[i]
    r.push({
      form,
      errors: errors[i] || initialErrorDict(form),
    })
  }
  return r
}

export function isFormData(val) {
  return (typeof FormData !== 'undefined') && (val instanceof FormData)
}

export function isArrayBuffer(val) {
  return (typeof ArrayBuffer !== 'undefined') && (val instanceof ArrayBuffer)
}

export function isFile(val) {
  return (typeof File !== 'undefined') && (val instanceof File)
}