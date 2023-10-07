<template>
  <div>
    <!-- 库存位下拉框 -->
    <el-select
      v-model="value"
      placeholder="请选择库存位"
      :loading="loading"
      clearable
      :disabled="isDisabled"
      @visible-change="visibleChange"
      @change="changSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.name"
        :value="isBinding?item.location:item.id"
      />
    </el-select>
  </div>
</template>

<script>
import { locationNameList } from '@/api/base_w_two'
import { getMaterialLocationBinding } from '@/api/shelf-material-binding'
export default {
  props: {
    //  created里面加载
    createdIs: {
      type: Boolean,
      default: false
    },
    defaultVal: {
      type: [Number, String],
      default: null
    },
    isEnable: { // 是否只显示启用
      type: Boolean,
      default: false
    },
    isDisabled: { // 是否只读
      type: Boolean,
      default: false
    },
    isBinding: { // 是否是物料绑定库存位
      type: Boolean,
      default: false
    },
    materialNo: { // 物料编码
      type: String,
      default: ''
    },
    materialName: { // 物料名字
      type: String,
      default: ''
    }
  },
  data() {
    return {
      value: this.defaultVal || null,
      loading: false,
      options: []
    }
  },
  watch: {
    defaultVal(val) {
      this.value = val || null
    },
    materialNo(val) {
      this.getList()
    }
  },
  created() {
    if (this.createdIs && !this.isBinding) {
      this.getList()
    }
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        let listData
        if (this.isBinding) {
          const obj = { spare_no: this.materialNo, material_name: this.materialName, all: 1 }
          const { results } = await getMaterialLocationBinding(obj)
          listData = results || []
        } else {
          listData = await locationNameList('get')
        }
        if (this.isEnable) {
          let arr = []
          arr = listData.filter(D => D.used_flag === 1)
          listData = arr
        }
        this.options = listData || []
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
    changSelect(val) {
      let arr = []
      if (this.isBinding) {
        arr = this.options.filter(D => D.location === val)
      } else {
        arr = this.options.filter(D => D.id === val)
      }
      this.$emit('changSelect', arr[0])
    }
  }
}
</script>

<style>

</style>
