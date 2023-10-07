<template>
  <div style="display:flex;margin-top:2px">
    <!-- <el-button type="success" size="mini">查看全部</el-button> -->
    <el-pagination
      v-if="oldPage"
      :disabled="true"
      :current-page.sync="_currentPage"
      layout="total,prev,pager,next"
      :page-size="pageSize"
      :total="total"
      @current-change="currentChange($event,pageSize)"
    />
    <div
      v-else
      style="display:flex"
      class="page-style"
    >
      <!-- <el-select
        v-model="pageSize"
        style="width:110px"
        size="mini"
        placeholder="请选择"
        @change="currentChange(1,$event)"
      >
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.name"
          :value="item.id"
        />
      </el-select>
      <el-pagination
        :current-page.sync="_currentPage"
        layout="total,prev,pager,next"
        :page-size="pageSize"
        :total="total"
        @current-change="currentChange($event,pageSize)"
      /> -->

      <el-pagination
        :current-page="_currentPage"
        :page-sizes="options"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background
        @size-change="currentChange(1,$event)"
        @current-change="currentChange($event,pageSize)"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    // 总页数，需要传进来
    total: {
      type: Number,
      default: 0
    },
    // 统一的当前展示多少页
    pageSizeProps: {
      type: Number,
      default: 10
    },
    currentPage: {
      type: Number,
      default: 1
    },
    oldPage: { // 默认只显示页面数据总数
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      pageSize: this.pageSizeProps,
      options: [10, 50, 100]
    }
  },
  computed: {
    _currentPage: {
      get() {
        return this.currentPage
      },
      set() {
        return 1
      }
    }
  },
  methods: {
    currentChange(page, page_size) {
      if (page_size) {
        this.pageSize = page_size
      }
      if (this.oldPage) {
        this.$emit('currentChange', page)
        return
      }
      this.$emit('currentChange', page, page_size)
    }
  }
}
</script>

<style lang="scss">
// .page-style{
//   .el-input,.el-select{
//     width:120px !important;
//   }
// }
</style>
