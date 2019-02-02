<template>
<v-layout row wrap class="pt-4" justify-center>
  <v-flex xs12 sm12>
    <v-card class="pa-3">
      <v-card-title primary-title class="pa-0">
        <h2 class="headline mb-0">パスワードの初期化</h2>
      </v-card-title>
      <v-card-text>
        登録に利用されたメールアドレスを入力してください。入力頂いたメールアドレスにパスワードリセット用のリンクを送信しますので、そちらからパスワードの再登録を実施してください。
      </v-card-text>
      <v-card-text>
        <div class="email mt-3">
          <non-field-errors :errors="errors" />
          <v-form ref="form" v-model="valid" lazy-validation>
            <my-input v-model="form.email" type="email" label="Email" :errors="errors.email" required autocomplete @keypress.enter.native="submit"></my-input>
          </v-form>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn flat color @click="submit">submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-flex>
</v-layout>
</template>

<script>
export default {
  async asyncData({ store, error }) {
    if (store.getters['account/isLoggedIn']) {
      error({ status: 400, statusCode: 400, message: 'ログアウトしてから再度アクセスください' })
      return
    }
    return {
      valid: false,
      form: {
        email: '',
      },
      errors: {},
    }
  },
  created() {
    this.$form.init()
  },
  methods: {
    async submit() {
      try {
        await this.$http.reset().request(this.form).then(res => res.data)
        this.$toast.success("指定のメールアドレスにパスワードリセット用リンクを送信しました。", { top: true })
      } catch (err) {
        this.$form.handleError(err)
      }
    }
  }
}
</script>
