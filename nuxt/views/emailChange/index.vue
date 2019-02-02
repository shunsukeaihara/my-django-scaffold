<template>
<div>
</div>
</template>

<script>
export default {
  props: {
    token: { type: String, required: true }
  },
  async asyncData({ app: { $http }, params: { token }, redirect, store }) {
    if (store.getters['account/isLoggedIn']) {
      try {
        let data = await $http.emailChange(token).validate().then(res => res.data)
        await store.dispatch("tokenInfo/setEmailChangeInfo", { token: token, email: data.email, error: null })
      } catch (err) {
        await store.dispatch("tokenInfo/setEmailChangeInfo", {
          token: token,
          email: null,
          error: {
            detail: err.response.data.detail,
            status: err.response.status
          }
        })
      }
    }
    redirect('/emailchange/')
  }
}
</script>
