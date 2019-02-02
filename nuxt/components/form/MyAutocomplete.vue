<template>
<v-autocomplete class="my-select" v-on="$listeners" v-bind="props" :error="hasErrors || error" v-model="model">
  <slot name="no-data" slot="no-data" v-if="hasNoDataSlot">
  </slot>
</v-autocomplete>
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
    hasNoDataSlot() {
      return this.$slots['no-data'];
    }
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
