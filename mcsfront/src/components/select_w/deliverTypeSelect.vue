<template>
  <div>
    <!-- 发货类型 -->
    <el-select
      v-model="value"
      placeholder="请选择发货类型"
      clearable
      @visible-change="visibleChange"
      @change="changeSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.global_name"
        :value="item.id"
      />
    </el-select>
  </div>
</template>

<script>
import { globalCodesUrl } from '@/api/base_w'
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
    }
  },
  data() {
    return {
      value: '',
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
      this.value = this.defaultVal
    }
  },
  methods: {
    async getList() {
      try {
        const data = await globalCodesUrl('get', { params: { all: 1, class_name: '发货类型' }})
        this.options = data.results || []
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
