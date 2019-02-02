<template>
<div></div>
</template>

<script>
export default {
  props: {
    token: { type: String, required: true }
  },
  created() {
    this.$form.init()
  },
  async asyncData({ app: { $http }, params: { token }, redirect, store }) {
    if (!store.getters['account/isLoggedIn']) {
      try {
        let data = await $http.reset(token).validate().then(res => res.data)
        await store.dispatch("tokenInfo/setPasswordResetInfo", { token: token, email: data.email, error: null })
      } catch (err) {
        console.log(err.response.data.detail)
        await store.dispatch("tokenInfo/setPasswordResetInfo", {
          token: token,
          email: null,
          error: {
            detail: err.response.data.detail,
            status: err.response.status
          }
        })
      }
    }
    redirect('/reset')
  }
}
</script>
