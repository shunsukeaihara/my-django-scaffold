<template>
<div class="error-page">
  <div class="error-info">
    <h1 class="error-code">{{ error.status || error.statusCode || 500 }}</h1>
    <div class="error-wrapper-message">
      <h2 class="error-message">{{ error.message || 'Internal Server Errror' }}</h2>
    </div>
    <nuxt-link class="error-link" to="/">Back to the home page</nuxt-link>
  </div>
</div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'nuxt-error',
  props: ['error'],
  head() {
    return {
      title: this.error.message || 'An error occured',
    }
  },
  mounted() {
    if (this.error.status === 401) {
      // 401場合、トークンが無効になっている可能性があるのでログアウトする
      this.logout()
    }
  },
  methods: {
    ...mapActions('account', ['logout']),
  },
}
</script>

<style scoped>
.error-page {
  color: #000;
  background: #fff;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: absolute;
  font-family: "SF UI Text", "Helvetica Neue", "Lucida Grande";
  text-align: center;
}

.error-info {
  position: absolute;
  top: 50%;
  left: 50%;
  -webkit-transform: translate(-50%, -50%);
  -moz-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  -o-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

.error-code {
  display: inline-block;
  font-size: 24px;
  font-weight: 500;
  vertical-align: top;
  border-right: 1px solid rgba(0, 0, 0, 0.298039);
  margin: 0px 20px 0px 0px;
  padding: 10px 23px;
}

.error-wrapper-message {
  display: inline-block;
  text-align: left;
  line-height: 49px;
  height: 49px;
  vertical-align: middle;
}

.error-message {
  font-size: 14px;
  font-weight: normal;
  margin: 0px;
  padding: 0px;
}

.error-link {
  color: #00BCD4;
  font-weight: normal;
  text-decoration: none;
  font-size: 14px;
}
</style>
