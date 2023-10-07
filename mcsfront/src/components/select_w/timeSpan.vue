<template>
  <div>
    <!-- 时间跨度下拉框 -->
    <el-select
      v-model="value"
      placeholder="请选择时间跨度"
      @visible-change="visibleChange"
      @change="changeSelect"
    >
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item.name"
        :value="item.id"
        :disabled="item.disabled"
      />
    </el-select>
  </div>
</template>

<script>
// import { testTypes } from '@/api/base_w'
export default {
  props: {
    defaultVal: {
      type: Number,
      default: null
    },
    dayType: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      value: this.defaultVal,
      options: [
        {
          id: 1,
          name: '班次'
        },
        {
          id: 2,
          name: '日'
        },
        // {
        //   id: 3,
        //   name: '周'
        // },
        {
          id: 3,
          name: '月'
        }
      ]
    }
  },
  watch: {
    dayType(val) {
      if (val) {
        this.value = this.value === 1 && val === 1 ? 2 : this.value
        this.$set(this.options[0], 'disabled', val !== 2)
        this.$emit('changeSelect', this.value)
      }
    }
  },
  methods: {
    async getList() {
      try {
        // const { results } = await testTypes('get', null, { params: { all: 1 }})
        // this.options = results || []
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
    //   if (val && this.options.length === 0) {
    //     this.getList()
    //   }
    },
    changeSelect(val) {
      this.$emit('changeSelect', val)
    }
  }
}
</script>

<style>

</style>
