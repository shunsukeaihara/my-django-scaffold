import changeCase from 'change-case'

function _changePropCase(obj, fn) {
  if (obj instanceof Array) {
    return _changePropCaseArray(obj, fn)
  } else if (typeof obj === 'object') {
    return _changePropCaseObject(obj, fn)
  }
  return obj
}

function _changePropCaseObject(obj, fn) {
  if (!obj) {
    return obj
  }
  let r = {}
  Object.keys(obj).forEach(k => {
    r[fn(k)] = _changePropCase(obj[k], fn)
  })
  return r
}

function _changePropCaseArray(arr, fn) {
  return arr.map(x => _changePropCase(x, fn))
}

function camel(obj) {
  return _changePropCase(obj, changeCase.camel)
}

function snake(obj) {
  return _changePropCase(obj, changeCase.snake)
}

export default {
  camel,
  snake,
}