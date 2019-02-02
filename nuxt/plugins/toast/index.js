import Vue from 'vue'
import toast from './MyToast.vue'

let Toast = Vue.extend(toast)

function getContainer() {
  let div = document.querySelector('.toasts')
  if (div) return div
  div = document.createElement('div')
  div.classList.add('toasts')
  document.body.appendChild(div)
  return div
}

export default (context, inject) => {
  let show = (text, options = null) => {
    let vm = new Toast({ propsData: { text, options } })
    let div = getContainer()
    let el = document.createElement('div')
    div.appendChild(el)
    vm.$mount(el)
  }
  show.info = (text, opts) => { show(text, Object.assign({ color: 'info' }, opts || {})) }
  show.success = (text, opts) => { show(text, Object.assign({ color: 'success' }, opts || {})) }
  show.error = (text, opts) => { show(text, Object.assign({ color: 'error' }, opts || {})) }

  inject('toast', show)
}