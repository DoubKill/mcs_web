<template>
  <div>
    <!-- 统计看版 -->
    <div class="abnormalBox">
      <div
        id="abnormalLine"
        style="width: 100%;height:450px;border-radius: 0"
      />
      <div class="abnormalRadio">
        <el-radio-group v-model="dimension" size="mini" @change="yieldBarChange">
          <el-radio-button label="日">日</el-radio-button>
          <el-radio-button label="月">月</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    <div class="SWBox">
      <div
        id="SWLine"
        style="width: 100%;height:420px;border-radius: 0"
      />
      <div class="SWRadio">
        <el-radio-group v-model="dimensionSW" size="mini" @change="SWChange">
          <el-radio-button label="日">日</el-radio-button>
          <el-radio-button label="月">月</el-radio-button>
        </el-radio-group>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { optionAbnormal, optionSW } from './echartsData'
import { taskCapacityAnalysis } from '@/api/base_w'
export default {
  name: 'StatisticalVersion',
  data() {
    return {
      dimension: '日',
      dimensionSW: '日'
    }
  },
  created() {
    this.optionAbnormal = optionAbnormal
    this.getList(1)
    this.optionSW = optionSW
    this.getList(2)
  },
  mounted() {
  },
  methods: {
    async getList(type) {
      try {
        this.loading = true
        const data = await taskCapacityAnalysis('get', null, { params: { query_type: type, dimension: type === 1 ? this.dimension : this.dimensionSW }})

        if (type === 1) {
          this.optionAbnormal.xAxis.data = data.h_axis
          this.optionAbnormal.series[0].data = data.v_data

          this.myChartAbnormalLine = echarts.init(document.getElementById('abnormalLine'))
          this.myChartAbnormalLine.setOption(this.optionAbnormal)
        }
        if (type === 2) {
          this.optionSW.xAxis.data = data.h_axis
          this.optionSW.series[0].data = data.v_data

          this.myChartSWLine = echarts.init(document.getElementById('SWLine'))
          this.myChartSWLine.setOption(this.optionSW)
        }

        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    yieldBarChange(val) {
      this.getList(1)
    },
    SWChange(val) {
      this.getList(2)
    }
  }
}
</script>

<style lang="scss" scoped>
    .abnormalBox{
        position: relative;
        margin-top:10px;
    }
    .abnormalRadio{
        position: absolute;
        top:13px;
        right:20px;
        z-index: 100;
    }
    .SWBox{
        position: relative;
    }
    .SWRadio{
        position: absolute;
        top:13px;
        right:20px;
        z-index: 100;
    }
</style>
