<template>
  <div>
    <!-- 检测指标;试验指标 -->
    <el-select
      v-model="value"
      placeholder="请选择试验指标"
      clearable
      :multiple="isMultiple"
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
import { testIndicators } from '@/api/base_w'
export default {
  props: {
    isMultiple: {
      type: Boolean,
      default: false
    },
    isCreated: {
      type: Boolean,
      default: false
    },
    defaultVal: {
      type: [String, Array],
      default: null
    }
  },
  data() {
    return {
      value: this.defaultVal || '',
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
        const data = await testIndicators('get', null, { all: 1 })
        this.options = data || []
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
      if (val && this.options.length === 0) {
        this.getList()
      }
    },
    changeSelect(val) {
      this.$emit('changeSelect', val)
    }
  }
}
</script>

<style>

</style>
