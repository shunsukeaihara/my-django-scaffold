<template>
<v-navigation-drawer :clipped="$vuetify.breakpoint.lgAndUp" app fixed v-model="showNavigation">
  <NavbarContentLoggedOut v-if="!isLoggedIn" />
  <NavbarContentLoggedIn v-else />
</v-navigation-drawer>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import NavbarContentLoggedIn from '@/components/NavbarContentLoggedin.vue'
import NavbarContentLoggedOut from '@/components/NavbarContentLoggedout.vue'
export default {
  components: {
    NavbarContentLoggedIn,
    NavbarContentLoggedOut,
  },
  computed: {
    ...mapGetters('screen', ['menuVisible']),
    ...mapGetters('account', ['isLoggedIn']),
    showNavigation: {
      get() { return this.menuVisible },
      set(value) { this.setMenuVisible(value) },
    },
  },
  data: () => ({}),
  methods: {
    ...mapActions('screen', ['setMenuVisible']),
  },
}
</script>

<style lang="scss" scoped>
</style>
