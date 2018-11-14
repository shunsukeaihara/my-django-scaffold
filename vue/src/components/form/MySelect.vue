<template>
<v-select class="my-select" outline v-on="$listeners" v-bind="props" :error="hasErrors || error" v-model="model"></v-select>
</template>
<script>
export default {
  props: {
    errors: Array,
    value: {},
    error: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    model: {
      get() { return this.value },
      set(value) { this.$emit('input', value) },
    },
    props() {
      return Object.assign({}, this.$attrs, { errorMessages: this.errors })
    },
    hasErrors() {
      return this.errors && this.errors.length !== 0
    },
  },
}
</script>

<style lang="scss">
/*
.my-select {
  .input-group__input {
    border: solid 1px rgb(178, 178, 179);
  }
}
*/
</style>
