<template>
<div>
  <v-text-field class="my-input" v-model="model" v-bind="props" v-on="$listeners" :error-messages="errors" @click.native="onClick" />
  <template v-if="solo">
    <small class="error--text" v-for="e in errors" :key="e">{{e}}</small>
  </template>
</div>
</template>

<script>
export default {
  props: {
    errors: Array,
    value: {},
    solo: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    props() {
      let solo = this.solo
      let r = { solo }
      Object.keys(this.$attrs).forEach(k => {
        let v = this.$attrs[k]
        if (k === 'errorMessages') return
        if (k === 'hideDetails') return
        if (v !== void(0)) r[k] = v
      })
      // if (!this.hasErrors) r.hideDetails = true
      return r
    },
    model: {
      get() { return this.value },
      set(value) { this.$emit('input', value) },
    },
    hasErrors() {
      return this.errors && this.errors.length !== 0
    },
  },
  methods: {
    onClick(e) {
      // NOTE: box styleの場合、box内の上部をクリックしてもfocusできない
      let target = e.target
      if (target && target.tagName === 'DIV') {
        let input = target.querySelector('input')
        if (input) input.focus()
      }
    },
  },
}
</script>

<style lang="scss">
/* .my-input {
   border: solid 1px grey;
   border-bottom: none;
   } */
</style>
