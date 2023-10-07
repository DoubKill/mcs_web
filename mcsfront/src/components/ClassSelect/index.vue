<template>
  <el-select
    v-model="className"
    :disabled="isDisabled"
    :clearable="isClearable"
    placeholder="请选择"
    @visible-change="visibleChange"
    @change="classChanged"
  >
    <el-option
      v-for="item in classOptions"
      :key="item.global_name"
      :label="item.global_name"
      :value="item.global_name"
    />
  </el-select>
</template>

<script>
import { class_arrange_url } from '@/api/display_static_fun'
export default {
  props: {
    isClearable: {
      type: Boolean,
      default: true
    },
    isDisabled: {
      type: Boolean,
      default: false
    },
    valueDefault: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      className: this.valueDefault || '',
      classOptions: []
    }
  },
  watch: {
    valueDefault(val) {
      this.className = val || ''
    }
  },
  methods: {
    getClasses() {
      class_arrange_url('get', {
        params: { }
      }).then(response => {
        this.classOptions = response.results
      })
    },
    visibleChange(visible) {
      if (visible) {
        this.getClasses()
      }
    },
    classChanged() {
      this.$emit('classSelected', this.className)
    }
  }
}
</script>
