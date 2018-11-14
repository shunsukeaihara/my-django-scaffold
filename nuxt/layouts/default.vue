<template>
<v-app>
  <Navbar />
  <v-toolbar app fixed :clipped-left="$vuetify.breakpoint.lgAndUp">
    <v-toolbar-side-icon @click.stop="toggleMenu"></v-toolbar-side-icon>
    <v-toolbar-title class="">
      <span class="font-weight-light">DJANGO SCAFFOLD</span>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn flat v-if="isLoggedIn" @click="execLogout">logout</v-btn>
      <v-btn flat v-if="showLogin" to="login">login</v-btn>
    </v-toolbar-items>
  </v-toolbar>
  <v-content>
    <nuxt />
  </v-content>
</v-app>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Navbar from "@/components/Navbar.vue"

export default {
  components: {
    Navbar
  },
  data() {
    return {
      //
    }
  },
  computed: {
    ...mapGetters("account", ['isLoggedIn']),
    showLogin() {
      if (!this.isLoggedIn && this.$route.name != "login") {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    ...mapActions("account", ['logout']),
    ...mapActions("screen", ['toggleMenu']),
    execLogout() {
      this.logout()
    }
  }
}
</script>
