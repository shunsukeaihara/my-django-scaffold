<template>
<div>
  <v-alert type="error" value="true" outline class="white" v-for="e in errors.nonFieldErrors" :key="e">{{e}}</v-alert>
</div>
</template>

<script>
export default {
  props: {
    errors: Object,
  },
}
</script>
