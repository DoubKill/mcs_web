<template>
  <!-- 原材料类别 -->
  <el-select
    :value="id"
    clearable
    placeholder="请选择"
    :disabled="isDisabled"
    @change="$emit('change', $event)"
    @visible-change="visibleChange"
  >
    <el-option
      v-for="item in materialTypeOptions"
      :key="item.id"
      :label="item.global_name"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { materialTypes } from '@/api/warehouse'
import { globalCodesUrl } from '@/api/base_w'
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
    },
    isCreated: {
      type: Boolean,
      default: false
    },
    isMaterial: { // 只显示原材料 去掉胶料段次
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      materialType: null,
      materialTypeOptions: []
    }
  },
  created() {
    if (this.isCreated) {
      this.getMaterialTypes()
    }
  },
  methods: {
    async getMaterialTypes() {
      try {
        const response = await materialTypes()
        const materialTypeOptions = response.results
        let resArr = materialTypeOptions
        let materialSegment
        if (this.isMaterial) {
          const response1 = await globalCodesUrl('get', { params: { class_name: '胶料段次' }})
          materialSegment = response1.results

          const set = materialSegment.map(item => item.global_name)
          resArr = materialTypeOptions.filter(item => !set.includes(item.global_name))
        }
        this.materialTypeOptions = resArr
      } catch (e) {
        //
      }
    },
    visibleChange(visible) {
      if (visible) {
        this.getMaterialTypes()
      }
    }
  }
}
</script>
