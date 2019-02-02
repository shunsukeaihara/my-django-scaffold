<script>
import Vue from 'vue'
const defaultLimit = 25
export default {
  name: 'MyDataTable',
  props: {
    fetchData: {
      type: Function,
      required: true,
    },
    query: {
      type: Object,
      default: null,
    },
  },
  data: () => ({
    loading: false,
    rowsPerPageItems: [25, 50, 100],
    pagination: {
      page: 1,
      rowsPerPage: defaultLimit,
      sortBy: null,
      descending: false,
    },
    items: [],
    totalItems: 0,
  }),
  computed: {
    limit() {
      return this.pagination.rowsPerPage
    },
    offset() {
      return (this.pagination.page - 1) * this.limit
    },
    ordering() {
      let { descending, sortBy } = this.pagination
      if (sortBy) {
        return descending ? `-${sortBy}` : sortBy
      } else {
        return null
      }
    },
  },
  watch: {
    query() {
      this.fetch()
    },
  },
  created() {
    let q = this.query
    if (q) {
      // NOTE: limit, offset等がonUpdatePaginationの初回呼び出しで上書きされるのを防ぐ
      let limit = defaultLimit
      if ('limit' in q) {
        this.pagination.rowsPerPage = q.limit
        limit = Number(q.limit)
      }
      if ('offset' in q) this.pagination.page = Math.ceil(q.offset / limit) + 1
    }
    this.fetch()
  },
  methods: {
    onUpdatePagination(data) {
      Object.assign(this.pagination, data)
      // let { descending, page, rowsPerPage, sortBy, totalItems } = data
      // console.log(
      //   'pagination',
      //   descending,
      //   page,
      //   rowsPerPage,
      //   sortBy,
      //   totalItems
      // )
      let query = Object.assign({}, this.query || {}, {
        offset: this.offset,
        limit: this.limit,
        ordering: this.ordering,
      })
      this.$emit('update:query', query)
    },
    async fetch() {
      this.loading = true
      try {
        let { results, count } = await this.fetchData(this.query)
        this.items = results
        this.totalItems = count
      } catch (err) {
        console.error(err)
        this.$toast.error('データの取得に失敗しました。')
      }
      this.loading = false
    },
  },
  render(createElement) {
    // console.log('render', JSON.stringify(this.pagination))
    let props = Object.assign({
        loading: this.loading,
        pagination: this.pagination,
        rowsPerPageItems: this.rowsPerPageItems,
        disableInitialSort: true,
        items: this.items,
        totalItems: this.totalItems,
      },
      this.$attrs
    )
    let on = Object.assign({
        'update:pagination': this.onUpdatePagination,
      },
      this.$listeners
    )
    return createElement(Vue.component('VDataTable'), {
      props,
      on,
      slots: this.$slots,
      scopedSlots: this.$scopedSlots,
    })
  },
}
</script>

<style>
.text1 {
  white-space: nowrap;
}

table.v-table thead td:not(:nth-child(1)),
table.v-table tbody td:not(:nth-child(1)),
table.v-table thead th:not(:nth-child(1)),
table.v-table tbody th:not(:nth-child(1)),
table.v-table thead td:first-child,
table.v-table tbody td:first-child,
table.v-table thead th:first-child,
table.v-table tbody th:first-child {
  padding: 0 4px;
}

.chips {
  padding: 10px 0;
}
</style>
