<template>
  <div>
    <!-- 试验方法下拉框 -->
    <el-select
      v-model="testMode"
      :filterable="add"
      allow-create
      default-first-option
      placeholder="请选择试验方法"
      :clearable="!createLoad"
      :loading="loading"
      @change="changeSelect"
      @visible-change="visibleChange"
    >
      <el-option
        v-for="itemoptions in options"
        :key="itemoptions.id"
        :label="itemoptions.name"
        :value="itemoptions.id"
      />
    </el-select>
  </div>
</template>

<script>
import { testSubTypes } from '@/api/base_w'
export default {
  props: {
    testmodeprop: {
      type: String,
      default() {
        return null
      }
    },
    // 指标 quota
    testTypeId: {
      type: Number,
      default: null
    },
    // 过滤方法  是类型过滤true 指标过滤false
    isTypeFilter: {
      type: Boolean,
      default: false
    },
    // 类型
    newTestTypeId: {
      type: Number,
      default() {
        return null
      }
    },
    add: {
      type: Boolean,
      default: false
    },
    createLoad: {
      type: Boolean,
      default: false
    },
    isRequired: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      options: [],
      testMode: this.testmodeprop || '',
      loading: false
    }
  },
  computed: {
  },
  watch: {
    newTestTypeId(val) {
      this.options = []
      if (val) {
        this.getList()
      }
    }
  },
  created() {
    if (this.createLoad) {
      this.getList()
    }
  },
  methods: {
    changeSelect(val) {
      if (this.add) {
        const arr = this.options.filter(D => D.id === val)
        // 传名称
        this.$emit('changeSelect', arr.length > 0 ? arr[0].name : val)
      } else {
        // 传id
        this.$emit('changeSelect', val)
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await testSubTypes('get', null, { params: {
          test_indicator_id: this.testTypeId || '',
          test_type_id: this.newTestTypeId || '',
          all: 1
        }})
        this.options = data.results
        if (this.options.length > 0 && this.createLoad) {
          this.testMode = this.options[0].id
          this.$emit('changeSelect', this.options[0].id)
        }
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    visibleChange(bool) {
      if (bool && !this.createLoad) {
        if (this.isRequired && !this.newTestTypeId) {
          return
        }
        this.getList()
      }
    }
  }
}
</script>

<style>

</style>
