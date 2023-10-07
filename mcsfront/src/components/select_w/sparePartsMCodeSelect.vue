<template>
  <div>
    <!-- 备品备件物料编码下拉 -->
    <el-select
      v-model="value"
      filterable
      placeholder="请选择"
      :loading="loading"
      clearable
      :disabled="isDisabled"
      @visible-change="visibleChange"
      @change="changeSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item[labelName]"
        :value="item.id"
      />
    </el-select>
  </div>
</template>

<script>
import { sparepartsSpare } from '@/api/base_w_two'
export default {
  props: {
    //  created里面加载
    createdIs: {
      type: Boolean,
      default: false
    },
    defaultVal: {
      type: Number,
      default: null
    },
    labelName: {
      type: String,
      default: 'name'
    },
    isAllObj: { // 是否返回全部对象
      type: Boolean,
      default: false
    },
    isDisabled: { // 是否只读
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      value: this.defaultVal,
      loading: false,
      options: []
    }
  },
  watch: {
    defaultVal(val) {
      this.value = val
    }
  },
  created() {
    if (this.createdIs) {
      this.getList()
    }
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await sparepartsSpare('get', null, { params: { all: 1 }})
        this.options = data.results || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    visibleChange(val) {
      if (val && this.options.length === 0 && !this.createdIs) {
        this.getList()
      }
    },
    changeSelect(val) {
      if (this.isAllObj) {
        let arr = []
        arr = this.options.filter(D => D.id === val)
        this.$emit('changeSelect', arr[0])
        return
      }
      this.$emit('changeSelect', val)
    }
  }
}
</script>

<style>

</style>
