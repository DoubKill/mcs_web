<template>
  <el-select
    :value="id"
    clearable
    placeholder="请选择"
    @change="$emit('change', $event)"
    @visible-change="visibleChange"
  >
    <el-option
      v-for="item in processOptions"
      :key="item.id"
      :label="item.global_name"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { getProcesses } from '@/api/display_static_fun'
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
    }
  },
  data() {
    return {
      processOptions: []
    }
  },
  created() {
    this.getProcessOptions()
  },
  methods: {
    async getProcessOptions() {
      const response = await getProcesses('get')
      this.processOptions = response.results
    },
    visibleChange(visible) {
      if (visible) {
        this.getProcessOptions()
      }
    }
  }
}
</script>
