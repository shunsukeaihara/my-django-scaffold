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
          <h2 class="headline mb-0">メールアドレスを変更</h2>
        </v-card-title>
        <v-card-text>
          メールアドレスを{{email}}から{{newemail}}に変更します。
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn flat color @click="submit">変更する</v-btn>
          <v-spacer />
        </v-card-actions>
      </template>
    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  async asyncData({ store, error }) {
    if (!store.getters['account/isLoggedIn']) {
      // errorページに飛ばす
      error({ status: 400, statusCode: 400, message: 'ログインが必要です' })
      return
    }
    let emailChangeInfo = store.getters['tokenInfo/emailChangeInfo']
    return {
      token: emailChangeInfo.token,
      newemail: emailChangeInfo.email,
      tokenErr: emailChangeInfo.error
    }

  },
  computed: {
    ...mapGetters('account', ['email']),
  },
  methods: {
    ...mapActions('account', ['setUserInfo']),
    ...mapActions('tokenInfo', ['resetTokenInfo']),
    async submit() {
      try {
        let data = await this.$http.emailChange(this.token).change({}).then(res => res.data)
        await this.setUserInfo(data)
        this.resetTokenInfo()
        this.$toast.success(`メールアドレスを${this.newemail}に変更しました `)
        this.$router.push({ path: "/home" })

      } catch (err) {
        this.$form.handleError(err)
      }
    },
    async resend() {
      try {
        this.progress = true
        await this.$http.resend(this.token).then(res => res)
        this.progress = false
        this.$toast.success('再送信しました', { top: true })
        this.resetTokenInfo()
      } catch (err) {
        this.progress = false
        this.$toast.error('再送信に失敗しました', { top: true })
      }
    }
  }
}
</script>
