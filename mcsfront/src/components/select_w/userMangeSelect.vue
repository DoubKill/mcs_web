<template>
  <div>
    <!-- 用户管理下拉框 -->
    <el-select
      v-model="value"
      placeholder="请选择用户"
      clearable
      filterable
      :multiple="isMultiple"
      :style="{'width':widthPx}"
      @visible-change="visibleChange"
      @change="changeSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.username"
        :value="item.id"
      />
    </el-select>
  </div>
</template>

<script>
import { personnelsUrl } from '@/api/basics'
export default {
  props: {
    defaultVal: {
      type: [String, Number, Array],
      default: null
    },
    isCreated: {
      type: Boolean,
      default: false
    },
    isMultiple: {
      type: Boolean,
      default: false
    },
    widthPx: {
      type: [Number, String],
      default: 'auto'
    },
    sectionName: {
      type: String,
      default: '品质技术部'
    },
    isSuperuser: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      value: this.defaultVal,
      options: []
    }
  },
  watch: {
    defaultVal(val) {
      this.value = val || null
      this.getList()
    }
  },
  created() {
    if (this.isCreated) {
      this.getList()
    }
  },
  methods: {
    async getList() {
      try {
        const obj = {
          all: 1, section_name: this.sectionName
        }
        if (this.isSuperuser) {
          // 去掉超级管理员用户
          obj.is_superuser = false
        } else {
          delete obj.is_superuser
        }
        const { results } = await personnelsUrl('get', null, { params: obj })
        this.options = results || []
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
      if (val && this.options.length === 0) {
        this.getList()
      }
    },
    changeSelect(val) {
      if (this.isMultiple) {
        this.$emit('changeSelect', val)
        return
      }
      let arr = []
      arr = this.options.filter(D => D.id === val)
      this.$emit('changeSelect', arr[0])
    }
  }
}
</script>

<style>

</style>
