<template>
  <el-select
    :value="id"
    clearable
    placeholder="请选择"
    :disabled="isDisabled"
    @change="changeFun"
    @visible-change="visibleChange"
  >
    <el-option
      v-for="item in stageOptions"
      :key="item.id"
      :label="item.global_name"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { stage_global_url } from '@/api/display_static_fun'
export default {
  model: {
    prop: 'id',
    event: 'change'
  },
  props: {
    id: {
      type: [Number, String],
      required: false,
      default: undefined
    },
    isDisabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      stageOptions: []
    }
  },
  created() {
    this.getStageOptions()
  },
  methods: {
    async getStageOptions() {
      const response = await stage_global_url('get')
      this.stageOptions = response.results
    },
    changeFun(id) {
      this.$emit('change', id)
      const arr = this.stageOptions.filter(D => D.id === id)
      this.$emit('changeFun', arr[0])
    },
    visibleChange(visible) {
      // if (visible) {
      //   this.getStageOptions()
      // }
    }
  }
}
</script>
