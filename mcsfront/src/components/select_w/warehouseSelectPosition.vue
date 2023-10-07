<template>
  <div>
    <!-- 仓库位置 出库口下拉 -->
    <el-select
      v-model="value"
      placeholder="请选择"
      :loading="loading"
      :clearable="isClear"
      no-data-text="暂无启用的"
      @visible-change="visibleChange"
      @change="changSelect"
    >
      <el-option
        v-for="item in options"
        :key="rawMaterial||drussDelivery?item.station_no:item.id"
        :label="rawMaterial||drussDelivery?item.station:item.name"
        :value="rawMaterial||drussDelivery?item.station_no:item.id"
      />
    </el-select>
  </div>
</template>

<script>
import { stationInfo, stationInfoRawMaterial, drussPlanManagementStations } from '@/api/warehouse'
export default {
  props: {
    optionsList: { // 从父组件传过来的值
      type: Array,
      default() {
        return []
      }
    },
    //  created里面加载
    createdIs: {
      type: Boolean,
      default: false
    },
    assignType: { // 指定出库
      type: Boolean,
      default: false
    },
    defaultVal: {
      type: [Number, String],
      default: null
    },
    // 是否可清空
    isClear: {
      type: Boolean,
      default: false
    },
    warehouseName: {
      type: String,
      default: null
    },
    startUsing: { // 只显示启用的
      type: Boolean,
      default: false
    },
    rawMaterial: { // 是不是原材料出库
      type: Boolean,
      default: false
    },
    drussDelivery: { // 是不是炭黑出库
      type: Boolean,
      default: false
    },
    show: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      value: null,
      loading: false,
      options: []
    }
  },
  watch: {
    defaultVal(val) {
      this.value = val || null
    },
    warehouseName(val) {
      this.value = ''
    },
    show(val) {
      if (val) {
        if (this.optionsList.length > 0) {
          this.options = this.optionsList
        }

        if (this.rawMaterial && this.createdIs && !this.assignType) {
          const a = localStorage.getItem('ycl-station')
          this.value = a ? JSON.parse(a).station_no : ''
          this.$emit('changSelect', this.options.filter(D => D.station_no === this.value)[0])
          return
        }
        if (this.drussDelivery && this.createdIs && !this.assignType) {
          const a = localStorage.getItem('th-station')
          this.value = a ? JSON.parse(a).station_no : ''
          this.$emit('changSelect', this.options.filter(D => D.station_no === this.value)[0])
          return
        }
      }
    }
  },
  created() {
    if (this.createdIs) {
      if (this.optionsList.length > 0) {
        this.options = this.optionsList
      } else {
        this.getList()
      }
    }
  },
  methods: {
    async getList() {
      try {
        if (!this.warehouseName) {
          this.options = []
          return
        }

        let data = []
        // if (this.optionsList.length === 0) {
        this.loading = true
        let _api
        if (this.rawMaterial) {
          _api = stationInfoRawMaterial
        } else if (this.drussDelivery) {
          _api = drussPlanManagementStations
        } else {
          _api = stationInfo
        }
        data = await _api({ all: 1, warehouse_name: this.warehouseName })
        this.loading = false
        // } else {
        //   data = this.optionsList
        // }

        if (this.startUsing && !this.rawMaterial && !this.drussDelivery) {
          this.options = data.filter(D => { return D.use_flag })
          return
        }
        this.options = data || []
        if (this.warehouseName === '混炼胶库' && this.createdIs) {
          const a = localStorage.getItem('hl-station')
          const value = a ? JSON.parse(a).id : ''
          if (this.value || (!value && this.value === value)) {
            return
          }
          this.value = a ? JSON.parse(a).id : ''
          this.$emit('changSelect', this.options.filter(D => D.id === this.value)[0])
          return
        }
        if (this.rawMaterial && this.createdIs && !this.assignType) {
          const a = localStorage.getItem('ycl-station')
          const value = a ? JSON.parse(a).id : ''
          if (this.value || (!value && this.value === value)) {
            return
          }
          this.value = a ? JSON.parse(a).station_no : ''
          this.$emit('changSelect', this.options.filter(D => D.station_no === this.value)[0])
          return
        }
        if (this.drussDelivery && this.createdIs && !this.assignType) {
          const a = localStorage.getItem('th-station')
          const value = a ? JSON.parse(a).id : ''
          if (this.value || (!value && this.value === value)) {
            return
          }
          this.value = a ? JSON.parse(a).station_no : ''
          this.$emit('changSelect', this.options.filter(D => D.station_no === this.value)[0])
          return
        }
        if (this.createdIs) {
          this.$emit('changSelect', {})
        }
      } catch (e) {
        this.loading = false
      }
    },
    visibleChange(val) {
      if (val) {
        this.getList()
      }
    },
    changSelect(val) {
      if (this.rawMaterial) { // 原材料出库 station_no
        arr = this.options.filter(D => D.station_no === val)
        this.$emit('changSelect', arr[0])
        return
      }
      if (this.drussDelivery) { // 炭黑出库 station_no
        arr = this.options.filter(D => D.station_no === val)
        this.$emit('changSelect', arr[0])
        return
      }
      let arr = []
      arr = this.options.filter(D => D.id === val)
      this.$emit('changSelect', arr[0])
    }
  }
}
</script>

<style>

</style>
