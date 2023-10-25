<template>
  <div class="">
    <!-- 在制产能汇总 -->
    <div class="selectStyle" v-if="!bigScreen">
      线体：
      <el-select v-model="route_name" clearable size="small" placeholder="请选择" @change="getList" @visible-change="visibleChange">
        <el-option v-for="item in lineList" :key="item" :label="item" :value="item" />
      </el-select>
    </div>
    <div style="width:98%;margin-top:10px">
      <div id="RealTimeBar" style="height:300px" />
      <div id="RealTimeBar1" style="height:300px;margin-top:8px" />
    </div>

    <h2 class="paddingBox paddingBoxTitle">实时在制</h2>
    <el-table stripe style="width: 98%" class="paddingBox" :data="tableData" border>
      <el-table-column prop="route_name" label="定线值" min-width="10">
      </el-table-column>
      <el-table-column :label="itemH&&itemH.process_name?itemH.process_name:''" v-for="itemH in heardList" :key="itemH.id">
        <el-table-column label="AGV" min-width="10">
          <template slot-scope="{row}">
            {{ row[itemH.process_name]&&row[itemH.process_name].AGV?row[itemH.process_name].AGV:'' }}
          </template>
        </el-table-column>
        <el-table-column label="WIP" min-width="10">
          <template slot-scope="{row}">
            {{ row[itemH.process_name]&&row[itemH.process_name].WIP?row[itemH.process_name].WIP:'' }}
          </template>
        </el-table-column>
        <el-table-column label="机台" min-width="10">
          <template slot-scope="{row}">
            {{ row[itemH.process_name]&&row[itemH.process_name].EQUIP?row[itemH.process_name].EQUIP:'' }}
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>
    <h2 class="paddingBox paddingBoxTitle">累计产量</h2>
    <el-table border class="paddingBox" :data="tableData1" style="width: 98%" stripe>
      <el-table-column prop="route_name" label="定线值" width="80">
      </el-table-column>
      <el-table-column min-width="20" :label="itemH.process_name" v-for="itemH in heardList" :key="itemH.id">
        <template slot-scope="{row}">
          {{ row[itemH.process_name]?row[itemH.process_name]:'' }}
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="带料AGV" :visible.sync="dialogVisible" width="30%">
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
import echarts from 'echarts'
import { processSections } from '@/api/jqy'
import { inProcessMonitor, currentRoute } from '@/api/base_w'
export default {
  name: 'RealTime',
  data() {
    return {
      option: {
        title: {
          text: '实时在制',
          left: 'center'
        },
        legend: {
          data: ['WIP', 'AGV', '机台'],
          bottom: '0%'
        },
        xAxis: {
          data: [],
          name: '',
          axisLine: { onZero: true },
          splitLine: { show: false },
          splitArea: { show: false },
          axisLabel: {
            show: true,
            interval: 0
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: value => { return value }
          },
          name: '篮'
        },
        grid: {
          bottom: 50,
          right: 30,
          left: 100
        },
        series: [
          {
            name: 'WIP',
            type: 'bar',
            stack: '11',
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
            name: 'AGV',
            type: 'bar',
            stack: '11',
            barMaxWidth: 150,
            label: {
              normal: {
                show: true,
                color: '#fff'
              }
            },
            data: [],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 1, color: 'rgb(143 217 100)' }
            ])
          },
          {
            name: '机台',
            type: 'bar',
            stack: '11',
            barMaxWidth: 150,
            label: {
              normal: {
                show: true,
                color: '#fff'
              }
            },
            data: [],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 1, color: '#FC7213' }
            ])
          },
          {
            name: '总数量',
            type: 'bar',
            stack: '11',
            itemStyle: {
              barBorderColor: 'rgba(0,0,0,0)',
              color: 'rgba(0,0,0,0)'
            },
            label: {
              normal: {
                show: true,
                position: 'insideBottom',
                formatter: '{c}', // 显示的总数
                textStyle: { color: '#000' }
              }
            },
            data: []
          }
        ]
      },
      option1: {
        color: ['rgb(60,187,178)', 'rgb(143,217,100)', '#FC7213', '#73c0de', '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de'],
        title: {
          text: '实时累计产量(当班产量)',
          left: 'center'
        },
        legend: {
          data: [],
          bottom: '0%'
        },
        xAxis: {
          data: [],
          name: '',
          axisLine: { onZero: true },
          splitLine: { show: false },
          splitArea: { show: false },
          axisLabel: {
            show: true,
            interval: 0
          }
        },
        yAxis: {
          type: 'value', axisLabel: {
            formatter: value => { return value }
          },
          name: '片'
        },
        grid: {
          bottom: 50,
          right: 30,
          left: 100
        },
        series: []
      },
      tableData: [],
      heardList: [],
      tableData1: [],
      dialogVisible: false,
      items: [],
      agv_detail: [],
      route_name: '',
      lineList: [],
      bigScreen: ''
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/real-time' || this.$route.fullPath === '/translate/real-time') {
          this.getHeardList()
          this._setInterval = setInterval(d => {
            this.getHeardList()
          }, 5000)
        } else {
          window.clearInterval(this._setInterval)
        }
      },
      deep: true, // 深度监听
      immediate: true // 第一次初始化渲染就可以监听到
    }
  },
  mounted() {
    this.bigScreen = this.$route.fullPath === '/real-time' ? false : true
    this.realTimeBar = echarts.init(document.getElementById('RealTimeBar'))
    this.realTimeBar.setOption(this.option, true)

    this.realTimeBar1 = echarts.init(document.getElementById('RealTimeBar1'))
    this.realTimeBar1.setOption(this.option1, true)

    this.realTimeBar.on('click', (params) => {
      if (params.seriesName === 'AGV') {
        this.items = this.agv_detail ? this.agv_detail[params.name] : ''
        this.dialogVisible = true
      }
    })
    // this.getHeardList()
  },
  created() {
  },
  methods: {
    async getList() {
      try {
        const data = await inProcessMonitor('get', null, { params: { route_name: this.route_name } })
        this.agv_detail = data.agv_detail || []
        this.tableData = data.results || []
        let obj
        if (this.tableData.length > 0) {
          obj = this.tableData[0]
          this.tableData.splice(0, 1)
          this.tableData.push(obj)
        }
        // 图1
        let arr = []
        let arr1 = []  //WIP
        let arr2 = []  //AGV
        let arr4 = []  //机台
        let arr3 = []  //合计
        this.heardList.forEach(dd => {
          arr.push(dd.process_name)
          if (obj[dd.process_name]) {
            arr1.push(obj[dd.process_name].WIP ? obj[dd.process_name].WIP : '')
          } else {
            arr1.push('')
          }
          if (obj[dd.process_name]) {
            arr2.push(obj[dd.process_name].AGV ? obj[dd.process_name].AGV : '')
          } else {
            arr2.push('')
          }
          if (obj[dd.process_name]) {
            arr4.push(obj[dd.process_name].EQUIP ? obj[dd.process_name].EQUIP : '')
          } else {
            arr4.push('')
          }
          if (obj[dd.process_name]) {
            let a = obj[dd.process_name] ? obj[dd.process_name].WIP : 0
            let b = obj[dd.process_name] ? obj[dd.process_name].AGV : 0
            let c = obj[dd.process_name] ? obj[dd.process_name].EQUIP : 0
            arr3.push((a + b + c) ? (a + b + c) : '')
          } else {
            arr3.push('')
          }
        })
        this.option.xAxis.data = arr
        this.option.series[0].data = arr1
        this.option.series[1].data = arr2
        this.option.series[2].data = arr4
        this.option.series[3].data = arr3
        this.realTimeBar.setOption(this.option)
        // 图1 end

        this.tableData1 = data.productions || []
        let obj1 = this.tableData1[0]
        this.tableData1.splice(0, 1)
        this.tableData1.push(obj1)
        // 图2
        let productionsName = []
        let seriesObj = {
          name: '实际车次',
          type: 'bar',
          stack: '11',
          barMaxWidth: 150,
          label: {
            show: true,
            color: '#fff'
          },
          data: [],
          // color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          //   { offset: 1,  }
          // ])
        }
        let seriesArr = []
        let amountTo = {
          name: '总数量',
          type: 'bar',
          stack: '11',
          itemStyle: {
            barBorderColor: 'rgba(0,0,0,0)',
            color: 'rgba(0,0,0,0)'
          },
          label: {
            normal: {
              show: true,
              position: 'insideBottom',
              formatter: '{c}', // 显示的总数
              textStyle: { color: '#000' }
            }
          },
          data: []
        }  //合计
        this.tableData1.forEach(d => {
          let _seriesObj = null
          if (d.route_name !== '合计') {
            productionsName.push(d.route_name)
            _seriesObj = JSON.parse(JSON.stringify(seriesObj))
          } else {
            _seriesObj = JSON.parse(JSON.stringify(amountTo))
          }
          _seriesObj.name = d.route_name
          let arrProductions = []
          arr.forEach(dd => {
            if (d[dd]) {
              arrProductions.push(d[dd])
            } else {
              arrProductions.push('')
            }
          })
          _seriesObj.data = arrProductions
          seriesArr.push(_seriesObj)
        })
        this.option1.legend.data = productionsName
        this.option1.xAxis.data = arr
        this.option1.series = seriesArr
        this.realTimeBar1.setOption(this.option1, true)
      } catch (e) {
        //
      }
    },
    async getHeardList() {
      try {
        const data = await processSections('get', null, { params: { out_rail_flat: 1, all: 1 } })
        this.heardList = data || []

        this.getList()
      } catch (e) {
        //
      }
    },
    async getCurrentRouteList() {
      try {
        const data = await currentRoute('get', null, { params: { all_route: 1 } })
        this.lineList = data || []
      } catch (e) {
        //
      }
    },
    visibleChange(val) {
      if (val) {
        this.getCurrentRouteList()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .paddingBox{
    margin-left: 20px;
  }
  .paddingBoxTitle{
    text-align: center;
  }
  .selectStyle{
    padding:20px;
    padding-bottom:0;
  }
</style>