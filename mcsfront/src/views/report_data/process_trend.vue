<template>
  <div>
    <!-- 在制趋势 -->
    <div class="selectStyle">
      线体：
      <el-select style="margin-right:8px" v-model="route_name" size="small" placeholder="请选择" @change="getList" @visible-change="visibleChange" clearable>
        <el-option v-for="item in lineList" :key="item" :label="item" :value="item" />
      </el-select>
      工序段:
      <el-select v-model="section_name" size="small" placeholder="请选择" @change="getList" @visible-change="visibleChange1" clearable>
        <el-option v-for="item in sectionList" :key="item.id" :label="item.process_name" :value="item.process_name" />
      </el-select>
    </div>
    <div id="RealTimeBar" style="width: 100%;height:500px;margin-top:20px" />
  </div>
</template>

<script>
import { currentRoute, inProcessTrend } from '@/api/base_w'
import { processSections } from '@/api/jqy'
import echarts from 'echarts'
export default {
  name: 'ProcessTrend',
  data() {
    return {
      route_name: '',
      section_name: '',
      lineList: [],
      sectionList: [],
      option: {
        color: ['rgb(60,187,178)', 'rgb(143,217,100)', '#FC7213', '#73c0de', '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'],
        title: {
          text: '在制趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['WIP', 'AGV'],
          bottom: '0%'
        },
        grid: {
          bottom: 50
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: []
        },
        yAxis: {
          type: 'value',
          name: '车',
          minInterval: 1
        },
        series: [
          {
            name: 'WIP',
            type: 'line',
            data: [],
            smooth: true
          },
          {
            name: 'AGV',
            type: 'line',
            data: [],
            smooth: true
          }
        ]
      }
    }
  },
  async mounted() {
    this.realTimeBar = echarts.init(document.getElementById('RealTimeBar'))
    this.realTimeBar.setOption(this.option, true)

    await this.getCurrentRouteList(true)
    await this.getSectionList(true)
  },
  methods: {
    async getList() {
      try {
        const data = await inProcessTrend('get', null, { params: { route_name: this.route_name, process_name: this.section_name } })
        this.option.xAxis.data = data.title
        this.option.series[0].data = data.wip
        this.option.series[1].data = data.agv
        this.realTimeBar.setOption(this.option)
      } catch (e) {
        //
      }
    },
    async getCurrentRouteList(bool) {
      try {
        const data = await currentRoute('get', null, { params: { all_route: 1 } })
        this.lineList = data || []
      } catch (e) {
        //
      }
    },
    async getSectionList(bool) {
      try {
        const data = await processSections('get', null, { params: { all: 1, out_rail_flat: 1 } })
        this.sectionList = data || []
        if (bool) {
          this.getList()
        }
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
      if (val) {
        this.getCurrentRouteList(false)
      }
    },
    visibleChange1(val) {
      if (val) {
        this.getSectionList(false)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
  .selectStyle{
    padding:20px;
    padding-bottom:0;
  }
</style>