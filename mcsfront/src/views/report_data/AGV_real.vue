<template>
  <div>
    <!-- AGV实时在制 -->
    <div class="selectStyle">
      工艺段：
      <el-select style="margin-right:8px" v-model="route_name" clearable size="small" placeholder="请选择" @change="getList" @visible-change="visibleChange">
        <el-option v-for="item in lineList" :key="item.id" :label="item.process_name" :value="item.id" />
      </el-select>
    </div>
    <div id="AGVRealBar" style="width: 100%;height:500px;margin-top:20px" />

    <el-dialog :title="title" :visible.sync="dialogVisible" width="30%">
      <el-tag v-for="item in items" :key="item" type="" effect="dark">
        {{ item }}
      </el-tag>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关 闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { processSections } from '@/api/jqy'
import { agvInProcess } from '@/api/base_w'
import echarts from 'echarts'
export default {
  name: 'ProcessTrend',
  data() {
    return {
      route_name: '',
      lineList: [],
      option: {
        title: {
          text: 'AGV实时在制',
          left: 'center'
        },
        legend: {
          data: ['总带料AGV', '空闲带料AGV'],
          bottom: '0%'
        },
        grid: {
          bottom: 50,
          left: 80,
          right: 80
        },
        xAxis: {
          data: [],
          axisLabel: {
            //x轴文字的配置
            show: true,
            interval: 0
          }
        },
        yAxis: {
          type: 'value', axisLabel: {
            formatter: value => { return value }
          },
          name: '车',
          minInterval: 1
        },
        series: [
          {
            name: '总带料AGV',
            type: 'bar',
            barMaxWidth: 150,
            label: {
              show: true,
              color: '#fff'
            },
            data: [],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 1, color: 'rgb(60 187 178)' }
            ])
          },
          {
            name: '空闲带料AGV',
            type: 'bar',
            barMaxWidth: 150,
            label: {
              show: true,
              color: '#fff'
            },
            data: [],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 1, color: 'rgb(143 217 100)' }
            ])
          }
        ]
      },
      dialogVisible: false,
      agv_detail: [],
      items: [],
      title: ''
    }
  },
  mounted() {
    this.AGVRealBar = echarts.init(document.getElementById('AGVRealBar'))
    this.AGVRealBar.setOption(this.option)

    this.AGVRealBar.on('click', (params) => {
      this.title = params.seriesName
      if (params.seriesName === '总带料AGV') {
        this.items = this.agv_detail ? this.agv_detail[params.dataIndex].all_agv_list : []
        this.dialogVisible = true
      } else {
        this.items = this.agv_detail ? this.agv_detail[params.dataIndex].free_agv_list : []
        this.dialogVisible = true
      }
    })

    this.getList()
  },
  methods: {
    async getList() {
      try {
        const { results } = await agvInProcess('get', null, { params: { process: this.route_name } })
        let headList = []
        let arr1 = []
        let arr2 = []
        results.forEach(d => {
          headList.push(d.process_name)
          arr1.push(d.total_belt)
          arr2.push(d.free_agv)
        })
        this.option.xAxis.data = headList
        this.option.series[0].data = arr1
        this.option.series[1].data = arr2
        this.AGVRealBar.setOption(this.option)
        this.agv_detail = results
      } catch (e) {
        //
      }
    },
    async getCurrentRouteList() {
      try {
        const data = await processSections('get', null, { params: { all: 1, out_rail_flat: 1 } })
        this.lineList = data || []
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
      if (val) {
        this.getCurrentRouteList()
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