<template>
  <el-select
    v-model="usedType"
    clearable
    placeholder="请选择"
    @change="$emit('usedTypeChange', usedType)"
  >
    <el-option
      v-for="item in usedTypes"
      :key="item[0]"
      :label="item[1]"
      :value="item[0]"
    />
  </el-select>
</template>

<script>
export default {
  data() {
    return {
      usedTypes: [
        [1, '编辑'],
        [2, '提交'],
        [3, '校对'],
        [4, '启用'],
        [5, '驳回'],
        [6, '废弃'],
        [7, '停用']
      ],
      usedType: ''
    }
  }
}
</script>
