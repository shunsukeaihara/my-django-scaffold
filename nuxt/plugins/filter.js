import Vue from 'vue'
import moment from 'moment'
moment.locale('ja')

Vue.filter('datetime', (value, format = 'YYYY.MM.DD HH:mm') => {
  if (!value) return
  return moment(value).format(format)
})

Vue.filter('date', (value, format = 'YYYY.MM.DD') => {
  if (!value) return
  return moment(value).format(format)
})

Vue.filter('dateLocal', (value, format = 'LL') => {
  if (!value) return
  return moment(value).format(format)
})

Vue.filter('locale', (value) => {
  if (!value) return value
  return Number(value).toLocaleString()
})

Vue.filter('price', (value) => {
  if (!value) return
  return Math.floor(Number(value)).toLocaleString()
})

Vue.filter('toNumber', (value) => {
  return Number(value)
})