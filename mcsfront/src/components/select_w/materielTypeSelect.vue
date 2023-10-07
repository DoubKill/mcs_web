<template>
  <div>
    <!-- 物料类型下拉 -->
    <el-select
      v-model="value"
      placeholder="请选择物料类型"
      :loading="loading"
      filterable
      :allow-create="paramsType"
      :default-first-option="paramsType"
      clearable
      :disabled="isDisabled"
      :multiple="isMultiple"
      @change="changSelect"
      @visible-change="visibleChange"
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
import { classesListUrl } from '@/api/base_w'
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
    warehouseName: {
      type: String,
      default: ''
    },
    paramsType: { // 自定义参数
      type: Boolean,
      default: true
    },
    isMultiple: {
      type: Boolean,
      default: false
    },
    isDisabled: {
      type: Boolean,
      default: false
    },
    objAll: { // 是否返回全部
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
    },
    warehouseName(val) {
      // 仓库名称
      this.getList()
    }
  },
  created() {
    if (this.createdIs) {
      this.getList()
    }
  },
  methods: {
    async getList(query) {
      try {
        this.loading = true
        const obj = { all: 1, class_name: '原材料类别' }
        // if (!this.warehouseName) {
        //   delete obj.warehouseName
        // }
        const data = await classesListUrl('get', null, { params: obj })
        this.options = data.results || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    remoteMethod(query) {
      if (query !== '') {
        this.getList(query)
      } else {
        this.options = []
      }
    },
    visibleChange(val) {
      if (val && this.options.length === 0 && !this.createdIs) {
        this.getList()
      }
    },
    changSelect(val) {
      let str = ''
      if (this.paramsType) {
        let arr = []
        arr = this.options.filter(D => D.id === val)

        if (arr.length > 0) {
          str = arr[0].global_name
        } else {
          str = val
        }
        this.$emit('changSelect', str)
        return
      }

      if (this.objAll) {
        const arr1 = this.options.filter(D => D.id === val)
        this.$emit('changSelect', arr1[0])
        return
      }
      this.$emit('changSelect', val)
    }
  }
}
</script>

<style>

</style>
