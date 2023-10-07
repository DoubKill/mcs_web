<template>
  <el-select
    v-model="suggestion_desc"
    clearable
    placeholder="请选择"
    @visible-change="visibleChange"
    @change="change"
  >
    <el-option
      v-for="(item, index) in suggestionOptions"
      :key="index"
      :label="item"
      :value="item"
    />
  </el-select>
</template>

<script>
import { dealSuggestionView } from '@/api/material-deal-result'

export default {
  data() {
    return {
      suggestion_desc: '',
      suggestionOptions: []
    }
  },
  methods: {
    change(desc) {
      this.$emit('dealSuggestionChange', this.suggestion_desc)
    },
    async getDealSuggestion() {
      const response = await dealSuggestionView()
      this.suggestionOptions = response
    //   console.log(response)
    },
    visibleChange(visible) {
      if (visible) {
        this.getDealSuggestion()
      }
    }
  }
}
</script>
