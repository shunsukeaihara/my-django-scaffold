<template>
<v-container>
  <v-layout row wrap class="pt-4" justify-center>
    <v-flex xs12 sm6>
      <v-card class="pa-3">
        <v-card-title primary-title class="pa-0">
          <h2 class="headline mb-0">Login</h2>
        </v-card-title>
        <div class="login mt-3">
          <non-field-errors :errors="errors" />
          <v-form ref="form" v-model="valid" lazy-validation>
            <my-input v-model="form.email" type="email" label="E-mail" :errors="errors.email" required></my-input>
            <my-input v-model="form.password" type="password" label="Password" :errors="errors.password" required @keypress.enter.native="submit"></my-input>
          </v-form>
        </div>
        <v-card-actions>
          <v-spacer />
          <v-btn flat color @click="submit">submit</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
export default {
  data: () => ({
    valid: false,
    form: {
      password: '',
      email: '',
    },
    errors: {},
  }),
  created() {
    this.$form.init()
  },
  computed: {
    ...mapGetters("account", ["isLoggedIn"])
  },
  methods: {
    ...mapActions("account", ['login', 'setUserInfo']),
    async submit() {
      try {
        let data = await this.$http.auth.login(this.form).then(res => res.data)
        await this.setUserInfo(data)
        this.$router.push({ path: this.$route.query.next ? this.$route.query.next : "/home" })
      } catch (err) {
        this.$form.handleError(err)
      }
    }
  }
}
</script>

<style>
.login label {
  transform: translateY(-18px) scale(.75) !important;
}
</style>
