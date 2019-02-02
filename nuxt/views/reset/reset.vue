<template>
<v-layout row wrap class="pt-4" justify-center>
  <v-flex xs12 sm12>
    <v-card class="pa-3">
      <template v-if="tokenErr">
        <v-card-title primary-title class="pa-0">
          <h2 class="headline mb-0">{{tokenErr.detail}}</h2>
        </v-card-title>
        <v-card-actions v-if="tokenErr.status==410">
          <v-spacer />
          <v-btn flat color @click="resend">再送信</v-btn>
          <v-spacer />
        </v-card-actions>
        <v-progress-linear v-if='progress' :indeterminate="true"></v-progress-linear>
      </template>
      <template v-else>
        <v-card-title primary-title class="pa-0">
          <h2 class="headline mb-0">{{email}}のパスワードをリセット</h2>
        </v-card-title>
        <div class="login mt-3">
          <non-field-errors :errors="errors" />
          <v-form ref="form" v-model="valid" lazy-validation autocomplete="off">
            <my-input v-model="form.password1" type="password" label="New Password" :errors="errors.password1" required autocomplete="off"></my-input>
            <my-input v-model="form.password2" type="password" label="New Password(再入力)" :errors="errors.password2" required autocomplete="off" @keypress.enter.native="submit"></my-input>
          </v-form>
        </div>
        <v-card-actions>
          <v-spacer />
          <v-btn flat color @click="submit">submit</v-btn>
        </v-card-actions>
      </template>
    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  created() {
    this.$form.init()
  },
  async asyncData({ store, error }) {
    if (store.getters['account/isLoggedIn']) {
      // errorページに飛ばす
      error({ status: 400, statusCode: 400, message: 'ログアウトしてから再度アクセスください' })
      return
    }
    let passwordResetInfo = store.getters['tokenInfo/passwordResetInfo']
    return {
      form: { username: "", password1: '', password2: '' },
      errors: {},
      progress: false,
      token: passwordResetInfo.token,
      tokenErr: passwordResetInfo.error,
      email: passwordResetInfo.email,
      valid: false,
    }
  },
  methods: {
    ...mapActions('account', ['setUserInfo']),
    ...mapActions('tokenInfo', ['resetTokenInfo']),
    async submit() {
      try {
        await this.$http.reset(this.token).reset(this.form).then(res => res.data)
        this.$toast.success("正常にパスワードが変更されました。", { top: true })
        this.resetTokenInfo()
        this.$router.push({ path: "/login" })
      } catch (err) {
        this.$form.handleError(err)
      }
    },
    async resend() {
      try {
        this.progress = true
        await this.$http.resend(this.token).then(res => res)
        this.progress = false
        this.resetTokenInfo()
        this.$toast.success('再送信しました', { top: true })
      } catch (err) {
        this.progress = false
        this.$toast.error('再送信に失敗しました', { top: true })
      }
    }
  }
}
</script>
