<template>
<v-snackbar v-bind="options" v-model="visible">
  <div v-html="text"></div>
  <v-btn dark flat @click.native="visible = false">Close</v-btn>
</v-snackbar>
</template>

<script>
export default {
  props: {
    text: String,
    options: Object,
  },
  data: () => ({
    visible: true,
  }),
  watch: {
    visible(value) {
      if (!value) {
        setTimeout(() => {
          this.$destroy()
        }, 2000)
      }
    },
  },
}
</script>
