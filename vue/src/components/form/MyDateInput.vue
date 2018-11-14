<template>
<v-layout wrap>
  <v-flex xs4 class="pr-3">
    <my-input ref="year" label="西暦" v-model="year" suffix="年" :error="hasError" mask="####" v-bind="$attrs" @input="onInputY" @blur="onBlur"></my-input>
  </v-flex>
  <v-flex xs4 class="px-3">
    <my-input ref="month" v-model="month" suffix="月" :error="hasError" mask="##" v-bind="$attrs" @input="onInputM" @blur="onBlur" min="1" max="12"></my-input>
  </v-flex>
  <v-flex xs4 class="pl-3" v-show="type === 'date'">
    <my-input ref="date" v-model="date" suffix="日" :error="hasError" mask="##" v-bind="$attrs" @input="onInputD" @blur="onBlur" min="1" max="31"></my-input>
  </v-flex>
  <v-flex xs12 v-for="e in errorMessages" :key="e" class="error--text"><small>{{e}}</small></v-flex>
</v-layout>
</template>

<script>
import { padStart } from 'lodash'
export default {
  props: {
    value: {},
    errorMessages: Array,
    type: {
      type: String,
      default: 'date',
    },
    error: Boolean,
  },
  computed: {
    hasError() {
      return this.error || this.errorMessages && this.errorMessages.length !== 0
    },
  },
  data: () => ({
    year: '',
    month: '',
    date: '',
  }),
  created() { this.setValues() },
  methods: {
    setValues() {
      // console.log('setValue', this.value)
      if (!this.value) return
      let [y, m, d] = this.value.split('-')
      this.year = y
      this.month = m
      this.date = d
    },
    onInputY(y) {
      if (this.$refs.month.$el.querySelector && String(y).length === 4) {
        let input = this.$refs.month.$el.querySelector('input')
        if (input) input.focus()
      }
    },
    onInputM(m) {
      if (this.type !== 'date') return
      if (this.$refs.date.$el.querySelector && String(m).length === 2) {
        let input = this.$refs.date.$el.querySelector('input')
        if (input) input.focus()
      }
    },
    onInputD(d) {},
    onBlur() {
      let m = this.month
      let d = this.date
      if (m) m = padStart(m, 2, '0')
      if (this.type === 'date') {
        if (d) d = padStart(d, 2, '0')
        this.$emit('input', `${this.year}-${m}-${d}`)
      } else {
        this.$emit('input', `${this.year}-${m}`)
      }
    },
  },
  watch: {
    value() { this.setValues() },

  },
}
</script>
