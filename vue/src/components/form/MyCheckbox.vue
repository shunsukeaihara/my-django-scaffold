<template>
<v-checkbox v-bind="$attrs" v-on="$listeners" v-model="model">
  <slot name="label" slot="label"></slot>
</v-checkbox>
</template>

<script>
export default {
  props: {
    value: {},
  },
  computed: {
    model: {
      set(value) {
        this.$emit('input', value)
      },
      get() {
        return this.value
      },
    },
  },
}
</script>
