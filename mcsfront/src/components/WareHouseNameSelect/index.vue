<template>
  <el-select
    v-model="name"
    clearable
    placeholder="请选择"
    @visible-change="visibleChange"
    @change="nameChanged"
  >
    <el-option
      v-for="item in nameOptions"
      :key="item"
      :label="item"
      :value="item"
    />
  </el-select>
</template>

<script>
import { warehouseNames } from '@/api/warehouse'

export default {
  data() {
    return {
      name: '',
      nameOptions: []
    }
  },
  methods: {
    getWarehouseNames() {
      warehouseNames().then(response => {
        this.nameOptions = response
      })
    },
    visibleChange(visible) {
      if (visible) {
        this.getWarehouseNames()
      }
    },
    nameChanged() {
      this.$emit('warehouseNameSelected', this.name)
    }
  }
}
</script>
