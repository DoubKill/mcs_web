<template>
  <el-select
    :value="id"
    clearable
    placeholder="请选择"
    @change="$emit('change', $event)"
    @visible-change="visibleChange"
  >
    <el-option
      v-for="item in stationTypeOptions"
      :key="item.id"
      :label="item.global_name"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { stationTypes } from '@/api/warehouse'
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
      stationTypeOptions: []
    }
  },
  created() {
    this.getStationTypes()
  },
  methods: {
    async getStationTypes() {
      const response = await stationTypes()
      this.stationTypeOptions = response.results
    //   stationTypes().then(response => {
    //     this.stationTypeOptions = response.results
    //   })
    },
    visibleChange(visible) {
      if (visible) {
        this.getStationTypes()
      }
    }
  }
}
</script>
