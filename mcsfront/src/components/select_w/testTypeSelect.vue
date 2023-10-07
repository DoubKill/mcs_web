<template>
  <div>
    <el-select
      v-model="value"
      placeholder="请选择试验类型"
      clearable
      @visible-change="visibleChange"
      @change="changeSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.name"
        :value="item.id"
      />
    </el-select>
  </div>
</template>

<script>
import { testTypes } from '@/api/base_w'
export default {
  props: {
    // 在created里面加载
    isCreated: {
      type: Boolean,
      default: false
    },
    defaultVal: {
      type: [Array, String, Number],
      default: null
    },
    obj: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      value: this.defaultVal,
      options: []
    }
  },
  watch: {
    defaultVal(val) {
      this.value = val
    }
  },
  created() {
    if (this.isCreated) {
      this.getList()
    }
  },
  methods: {
    async getList() {
      try {
        const { results } = await testTypes('get', null, { params: { all: 1 }})
        this.options = results || []
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
      if (val && this.options.length === 0 && !this.isCreated) {
        this.getList()
      }
    },
    changeSelect(val) {
      if (this.obj) {
        const arr = this.options.filter(D => D.id === val)
        this.$emit('changeSelect', arr.length > 0 ? arr[0] : null)
        return
      }
      this.$emit('changeSelect', val)
    }
  }
}
</script>

<style>

</style>
