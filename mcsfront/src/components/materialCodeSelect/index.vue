<template>
  <div>
    <!-- 原材料编码下拉 -->
    <el-select
      v-model="value"
      filterable
      placeholder="请选择"
      :loading="loading"
      clearable
      :disabled="isDisabled"
      :allow-create="isCreated"
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
import { materialsUrl } from '@/api/base_w'
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
    labelName: {
      type: String,
      default: 'material_no'
    },
    isAllObj: { // 是否返回全部对象
      type: Boolean,
      default: false
    },
    isDisabled: { // 是否只读
      type: Boolean,
      default: false
    },
    isCreated: { // 是可创建条目
      type: Boolean,
      default: false
    },
    objParams: {
      type: Object,
      default() {
        return {}
      }
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
        const obj = { all: 1 }
        Object.assign(obj, this.objParams)
        const data = await materialsUrl('get', null, { params: obj })
        this.options = data.results || []
        const arr = this.options.map(D => {
          D.material_str = '名称:' + D.material_name + '; ' + '编码:' + D.material_no + '; ' + '类型:' + D.material_type__global_name
          return D
        })
        this.options = arr
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    visibleChange(val) {
      if (val && !this.createdIs) {
        this.getList()
      }
    },
    changeSelect(val) {
      if (this.isAllObj) {
        let arr = []
        arr = this.options.filter(D => D.id === val)
        if (this.isCreated) {
          if (arr.length > 0) {
          // 返回物料编码名称
            this.$emit('changeSelect', arr[0].material_no)
            return
          } else {
            this.$emit('changeSelect', val)
            return
          }
        }
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
