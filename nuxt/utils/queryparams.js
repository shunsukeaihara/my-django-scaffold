import changeCase from 'change-case'

export function makeSortParam(sortBy, descending) {
  let snake = changeCase.snakeCase(sortBy)
  if (descending) {
    return `-${snake}`
  } else {
    return snake
  }
}