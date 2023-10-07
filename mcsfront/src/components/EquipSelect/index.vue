<template>
  <el-select
    v-model="equipId"
    clearable
    placeholder="请选择"
    :multiple="isMultiple"
    :disabled="isDisabled"
    @change="equipChanged"
    @visible-change="visibleChange"
  >
    <el-option
      v-for="item in equipOptions"
      :key="item.id"
      :label="item.equip_no"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { getEquip } from '@/api/banburying-performance-manage'

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
    isDisabled: {
      type: Boolean,
      default: false
    },
    defaultVal: {
      type: [String, Number, Array],
      default: null
    },
    // 设备类型
    equipType: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      equipId: this.defaultVal || '',
      equipOptions: []
    }
  },
  watch: {
    defaultVal(val) {
      this.equipId = val
    }
  },
  created() {
    if (this.isCreated) {
      this.getList()
    }
  },
  methods: {
    getList() {
      const obj = { all: 1 }
      if (this.equipType) {
        obj.category_name = this.equipType
      } else {
        delete obj.category_name
      }
      getEquip(obj).then(response => {
        this.equipOptions = response.results
      })
    },
    visibleChange(visible) {
      if (visible && this.equipOptions.length === 0) {
        this.getList()
      }
    },
    equipChanged(arr) {
      if (this.isMultiple) {
        this.$emit('equipSelected', arr)
        return
      }
      this.$emit('equipSelected', this.equipOptions.find(option => option.id === this.equipId))
    }
  }
}
</script>
