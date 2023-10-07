<template>
  <div :class="['homePage-container',bigScreen?'bigScreen':'']">
    <div v-if="bigScreen" class="head-top">
      <img src="@/assets/logoHeard.png" alt="">
      <div class="d-flex">
        <span class="decoration10" />
        <span class="decoration8" />
        <div class="title">
          <h2 style="font-size:30px;">中策橡胶安吉准备分厂 MES系统</h2>
          <span class="title-border" />
        </div>
        <span class="decoration8 decoration8-1" />
        <span class="decoration10" />
      </div>
      <h3 class="set-current-time">{{ currentTime }}</h3>
    </div>
    <el-row :gutter="20" style="font-weight:700;font-size:16px">
      <el-col :span="4">
        <el-card class="box-card">
          <!-- <div class="volumeBox"> -->
          <span :style="{'color':color[1]}">日计划量(车/吨)</span><br>
          <div class="volumeBoxChild" :style="{'color':color[0]}">
            <span v-if="overviewObj.plan_data">
              {{ overviewObj.plan_data.total_trains||'-' }}/{{ overviewObj.plan_data.total_weight||'-' }}
            </span>
            <span v-else>-</span>
            <!-- </div> -->
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="">
          <span :style="{'color':color[1]}">日总产量(车/吨)</span><br>
          <div class="volumeBoxChild" :style="{'color':color[0]}">
            <span v-if="overviewObj.actual_data">
              {{ overviewObj.actual_data.total_trains||'-' }}/{{ overviewObj.actual_data.total_weight||'-' }}
            </span>
            <span v-else>-</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="">
          <span :style="{'color':color[1]}">日入库量(车/吨)</span><br>
          <div class="volumeBoxChild" :style="{'color':color[0]}">
            <span v-if="overviewObj.inbound_data">
              {{ overviewObj.inbound_data.total_trains||'-' }}/{{ overviewObj.inbound_data.total_weight||'-' }}
            </span>
            <span v-else>-</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="">
          <span :style="{'color':color[1]}">日出库量(车/吨)</span><br>
          <div class="volumeBoxChild" :style="{'color':color[0]}">
            <span v-if="overviewObj.outbound_data">
              {{ overviewObj.outbound_data.total_trains||'-' }}/{{ overviewObj.outbound_data.total_weight||'-' }}
            </span>
            <span v-else>-</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="">
          <span :style="{'color':color[1]}">日合格率</span><br>
          <div class="volumeBoxChild" :style="{'color':color[0]}">{{ overviewObj.qualified_rate||'-' }}</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="">
          <span :style="{'color':color[1]}">日发货量(车/吨)</span><br>
          <div class="volumeBoxChild" :style="{'color':color[0]}">
            <span v-if="overviewObj.dispatch_data">
              {{ overviewObj.dispatch_data.total_weight||'-' }}/{{ overviewObj.dispatch_data.total_weight||'-' }}
            </span>
            <span v-else>-</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12" style="margin-top:5px;margin-bottom:10px">
        <el-card class="yieldBar">
          <div
            id="yieldBar"
            class="volumeBox"
            style="width: 100%;height:300px;flex:1;border-radius: 0"
          />
          <!-- <div class="yieldBarRadio">
            <el-radio-group v-model="yieldBarRadio" size="mini" @change="yieldBarChange">
              <el-radio-button label="1">本周</el-radio-button>
              <el-radio-button label="2">本月</el-radio-button>
            </el-radio-group>
          </div> -->
        </el-card>
      </el-col>
      <el-col :span="12" style="margin-top:5px;margin-bottom:10px">
        <el-card class="yieldBar">
          <div
            id="passRateLine"
            class="volumeBox"
            style="width: 100%;height:300px;flex:1;border-radius: 0"
          />
          <div class="yieldBarLine">
            <el-radio-group v-model="yieldBarRadio" size="mini" @change="yieldBarChange">
              <el-radio-button label="1">本周</el-radio-button>
              <el-radio-button label="2">本月</el-radio-button>
            </el-radio-group>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="relativeFa">
          <div
            id="finishChart"
            class="volumeBox"
            style="width: 100%;height:300px;"
          />
          <div class="absoluteFa">
            <el-tabs v-model="equipProduction.dimension" style="width:190px" @tab-click="handleClick('equipProduction')">
              <el-tab-pane label="总计" name="0" />
              <el-tab-pane label="今天" name="1" />
              <el-tab-pane label="昨天" name="2" />
            </el-tabs>
            <el-date-picker
              v-model="equipProduction.dateFinish"
              style="width:240px;"
              type="daterange"
              value-format="yyyy-MM-dd"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="handleClickDate($event,'equipProduction')"
            />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="relativeFa">
          <div
            id="shutdownBar"
            class="volumeBox"
            style="width: 100%;height:300px;"
          />
          <div class="absoluteFa">
            <el-tabs v-model="equipMaintenance.dimension" style="width:190px" @tab-click="handleClick('equipMaintenance')">
              <el-tab-pane label="本月" name="0" />
              <el-tab-pane label="今天" name="1" />
              <el-tab-pane label="昨天" name="2" />
            </el-tabs>
            <el-date-picker
              v-model="equipMaintenance.dateFinish"
              style="width:240px;"
              type="daterange"
              value-format="yyyy-MM-dd"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="handleClickDate($event,'equipMaintenance')"
            />
          </div>
        </el-card>
      </el-col>
      <!-- <el-col :span="24">
        <div
          id="OEEBar"
          class="volumeBox"
          style="width: 100%;height:300px;"
        />
      </el-col> -->
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { setDate } from '@/utils'
import { indexOverview, indexProductionAyalyze, indexEquipProductionAyalyze, indexEquipMaintenanceAyalyze } from '@/api/base_w_three'
import { globalCodesUrl } from '@/api/base_w'

export default {
  name: 'HomePageMain',
  components: {},
  data() {
    this.color = ['#188df0', '#E6A23C']
    this.chartSettings = {
      labelMap: {
        time: '时间',
        plan_trains: '计划车次',
        actual_trains: '实际生产车次'
      }
    }
    this.extend = {
      series: {
        label: { show: true, position: 'top' }
      }
    }
    this.chartSettingsCir = {
      radius: '90'
    }
    return {
      currentTime: setDate(null, true),
      yieldBarRadio: '1',
      equipProduction: {
        dimension: '1',
        dateFinish: [],
        st: '',
        et: ''
      },
      equipMaintenance: {
        dimension: '1',
        dateFinish: [],
        st: '',
        et: ''
      },
      getInfoData: {},
      overviewObj: {},
      optionYieldBar: {
        color: this.color,
        legend: {
          data: ['计划车次', '实际车次'],
          textStyle: {
            color: '#000'// 字体颜色
          }
        },
        title: {
          left: 'left',
          text: '产量分析',
          textStyle: { color: '#000' }
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLine: {
            lineStyle: {
              color: '#000',
              width: 1// 这里是为了突出显示加上的
            }
          }
        },
        yAxis: {
          name: '车',
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#000',
              width: 1// 这里是为了突出显示加上的
            }
          }
        },
        grid: {
          top: '25%',
          left: '3%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        series: [
          {
            name: '计划车次',
            type: 'bar',
            barMaxWidth: 150,
            data: [],
            showSymbol: false,
            itemStyle: {
              normal: {
                label: {
                  show: true,
                  position: 'top',
                  color: '#000'
                }}},
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgb(231 219 201)' },
              { offset: 0.5, color: 'rgb(239 196 131)' },
              { offset: 1, color: 'rgb(239 196 131)' }
            ])
          },
          {
            name: '加硫',
            type: 'line',
            label: {
              show: false
            },
            showSymbol: false,
            data: [],
            itemStyle: {
              normal: {
                color: 'rgba(128, 128, 128, 0)' // 柱状图颜色设为透明
              }
            }
          },
          {
            name: '无硫',
            type: 'line',
            label: {
              show: false
            },
            showSymbol: false,
            data: [],
            itemStyle: {
              normal: {
                color: 'rgba(128, 128, 128, 0)' // 柱状图颜色设为透明
              }
            }
          },
          {
            name: '实际车次',
            type: 'bar',
            barMaxWidth: 150,
            data: [],
            showSymbol: false,
            itemStyle: {
              normal: {
                label: {
                  show: true,
                  color: '#000'
                }}},
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          },
          {
            name: '加硫',
            type: 'line',
            data: [],
            showSymbol: false,
            itemStyle: {
              normal: {
                color: 'rgba(128, 128, 128, 0)' // 柱状图颜色设为透明
              }
            },
            label: {
              show: false
            }
          },
          {
            name: '无硫',
            type: 'line',
            showSymbol: false,
            data: [],
            label: {
              show: false
            },
            itemStyle: {
              normal: {
                color: 'rgba(128, 128, 128, 0)' // 柱状图颜色设为透明
              }
            }
          }
        ]
      },
      optionPassRateLine: {
        color: ['#8498f9'],
        title: {
          left: 'left',
          text: '综合合格率分析',
          textStyle: { color: '#000' }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            // type: 'cross'
          }
        },
        grid: {
          top: '25%',
          left: '3%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            axisTick: {
              alignWithLabel: true
            },
            data: [],
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 1
              }
            }
          }
        ],
        yAxis: {
          type: 'value',
          name: '%',
          axisLine: {
            show: true,
            lineStyle: {
              color: '#000',
              width: 1
            }
          },
          max: 100,
          min: 0
        },
        series: [
          {
            name: '综合合格率',
            type: 'line',
            data: [],
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(58,77,233,0.8)'
                },
                {
                  offset: 1,
                  color: 'rgba(58,77,233,0.1)'
                }
              ])
            },
            itemStyle: { normal: {
              label: { show: true, color: '#000' }}}
          },
          {
            name: '合格车数',
            type: 'line',
            showSymbol: false,
            data: [],
            itemStyle: {
              normal: {
                color: 'rgba(128, 128, 128, 0)' // 柱状图颜色设为透明
              }
            }
          },
          {
            name: '检测车数',
            type: 'line',
            data: [],
            showSymbol: false,
            itemStyle: {
              normal: {
                color: 'rgba(128, 128, 128, 0)' // 柱状图颜色设为透明
              }
            }
          }
        ]
      },
      optionFinishChart: {
        title: {
          left: 'left',
          text: '机台产量分析',
          textStyle: { color: '#000' }
        },
        legend: {
          data: ['实际车次', '计划车次'],
          x: 'left',
          y: 'left',
          padding: [5, 0, 0, 170],
          textStyle: {
            color: '#000' // 字体颜色
          }
        },
        color: ['rgb(121, 187, 255)', 'rgb(179, 216, 255)', '#E6A23C'],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            const firstParams = params[0]
            const sndParams = params[2]

            return firstParams.name + '<br>' + firstParams.seriesName + '：' + (firstParams.value ? firstParams.value : 0) + '<br>' +
            sndParams.seriesName + '：' + (sndParams.value ? sndParams.value : 0)
          }
        },
        grid: {
          left: '3%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          data: [],
          axisLine: {
            show: true,
            lineStyle: {
              color: '#000',
              width: 1
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '车',
          axisLine: {
            show: true,
            lineStyle: {
              color: '#000',
              width: 1
            }
          }
        },
        series: [
          {
            name: '实际车次',
            type: 'bar',
            stack: '11',
            barMaxWidth: 150,
            label: {
              show: true,
              color: '#000'
            },
            data: [],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' }
            ])
          },
          {
            name: '计划车次',
            type: 'bar',
            stack: '11',
            barMaxWidth: 150,
            label: {
              normal: {
                show: false,
                position: 'center'
              }
            },
            data: [],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgb(231 219 201)' },
              { offset: 0.5, color: 'rgb(239 196 131)' },
              { offset: 1, color: 'rgb(239 196 131)' }
            ])
          },
          // {
          //   name: '折线',
          //   type: 'line',
          //   data: [120, 132, 101, 134, 90, 230, 210]
          // },
          {
            name: '计划车次',
            type: 'bar',
            stack: '11',
            itemStyle: {
              barBorderColor: 'rgba(0,0,0,0)',
              color: 'rgba(0,0,0,0)'
            },
            label: {
              normal: {
                // offset: ['50', '80'],
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
      optionShutdownBar: {
        color: this.color,
        title: {
          left: 'left',
          text: '机台停机时间分析',
          textStyle: { color: '#000' }
        },
        grid: {
          left: '3%',
          right: '6%',
          bottom: '3%',
          top: '25%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLine: {
            show: true,
            lineStyle: {
              color: '#000',
              width: 1
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '分钟',
          axisLine: {
            show: true,
            lineStyle: {
              color: '#000',
              width: 1
            }
          }
        },
        series: [{
          data: [],
          name: '机台停机时间',
          type: 'bar',
          barMaxWidth: 150,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ]),
          itemStyle: { normal: {
            label: { show: true, position: 'top', color: '#000' }}}
        }]
      },
      optionOEEBar: {
        color: this.color,
        title: {
          left: 'center',
          text: '机台OEE分析',
          textStyle: { color: '#000' }
        },
        grid: {
          left: '3%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          name: '机台',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          lineStyle: {
            color: '#fff',
            width: 1// 这里是为了突出显示加上的
          }
        },
        yAxis: {
          type: 'value',
          name: '%',
          lineStyle: {
            color: '#fff',
            width: 1// 这里是为了突出显示加上的
          }
        },
        series: [{
          data: [120, 200, 150, 80, 70, 110, 130],
          type: 'bar',
          barMaxWidth: 150,
          itemStyle: { normal: { label: { show: true, position: 'top' }}}
        }]
      },
      modeType: true
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/homePage' || this.$route.fullPath === '/homePage/index') {
          this.bigScreen = this.$route.fullPath === '/homePage/index'
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
          }, 30000)
        } else {
          window.clearInterval(this._setInterval)
        }
      },
      deep: true, // 深度监听
      immediate: true // 第一次初始化渲染就可以监听到
    }
  },
  created() {
    this.bigScreen = this.$route.fullPath === '/homePage/index'
    setInterval(d => {
      this.currentTime = setDate(null, true)
    }, 1000)
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  mounted() {
    this.myChartYieldBar = echarts.init(document.getElementById('yieldBar'))
    this.myChartYieldBar.setOption(this.optionYieldBar)
    this.myChartPassRateLine = echarts.init(document.getElementById('passRateLine'))
    this.myChartPassRateLine.setOption(this.optionPassRateLine, true)
    this.myChartFinishChart = echarts.init(document.getElementById('finishChart'))
    this.myChartFinishChart.setOption(this.optionFinishChart)

    this.myChartShutdownBar = echarts.init(document.getElementById('shutdownBar'))
    this.myChartShutdownBar.setOption(this.optionShutdownBar)
    // this.myChartOEEBar = echarts.init(document.getElementById('OEEBar'))
    // this.myChartOEEBar.setOption(this.optionOEEBar)
  },
  methods: {
    async getList(bool, bool1, bool2) {
      // 哪个图 那个bool就设置为true
      let modelVal = []
      if (this.bigScreen) {
        try {
          const data = await globalCodesUrl('get', { params: { class_name: '首页参观展示切换（正常/参观）' }})
          const obj = data.results.find(d => d.use_flag)
          this.modeType = obj.global_name === '正常模式'
          modelVal = obj.description.split(',')
        } catch (e) {
          //
        }
      }
      try {
        const arr = await Promise.all([
          bool || bool1 || bool2 ? '' : indexOverview('get'),
          bool1 || bool2 ? '' : indexProductionAyalyze('get', null, { params: { dimension: this.yieldBarRadio }}),
          bool || bool2 ? '' : indexEquipProductionAyalyze('get', null, { params: this.equipProduction }),
          bool || bool1 ? '' : indexEquipMaintenanceAyalyze('get', null, { params: this.equipMaintenance })
        ])
        if (!bool1 && !bool2 && !bool) {
          this.overviewObj = arr[0]
        }
        if (!bool1 && !bool2) {
          // 第一个数据 第二个图
          const qualified_rate_data_rate = this.setVal(arr[1].qualified_rate_data, 'rate')
          const qualified_rate_data_qualified_count = this.setVal(arr[1].qualified_rate_data, 'qualified_count')
          const qualified_rate_data_total = this.setVal(arr[1].qualified_rate_data, 'total')
          if (this.modeType) {
            this.optionPassRateLine.series[0].data = qualified_rate_data_rate
            this.optionPassRateLine.series[1].data = qualified_rate_data_qualified_count
            this.optionPassRateLine.series[2].data = qualified_rate_data_total
          } else {
            this.optionPassRateLine.series[0].data = modelVal
            this.overviewObj.qualified_rate = modelVal[modelVal.length - 1] + '%'
          }

          this.optionPassRateLine.xAxis[0].data = arr[1].date_range
          if (this.bigScreen) {
            this.optionPassRateLine.xAxis[0].axisLine.lineStyle.color = '#fff'
            this.optionPassRateLine.yAxis.axisLine.lineStyle.color = '#fff'
            this.optionPassRateLine.title.textStyle.color = '#fff'
            this.optionPassRateLine.series[0].itemStyle.normal.label.color = '#fff'
          }
          this.myChartPassRateLine.setOption(this.optionPassRateLine, true)
        }
        if (!bool && !bool2) {
          // 第三个数据
          const plan_actual_actual_trains = this.setVal(arr[2].plan_actual_data, 'actual_trains', true)
          const plan_actual_diff_trains = this.setVal(arr[2].plan_actual_data, 'diff_trains', true)
          const plan_actual_plan_trains = this.setVal(arr[2].plan_actual_data, 'plan_trains', true)

          // 算y最大值
          const maxVal = Math.max(...plan_actual_plan_trains)
          const legMaxVal = maxVal.toString().length
          let str = '1'
          for (let index = 1; index < legMaxVal; index++) {
            str += '0'
          }
          if (this.bigScreen) {
            this.optionFinishChart.xAxis.axisLine.lineStyle.color = '#fff'
            this.optionFinishChart.yAxis.axisLine.lineStyle.color = '#fff'
            this.optionFinishChart.title.textStyle.color = '#fff'
            this.optionFinishChart.series[2].label.normal.textStyle.color = '#fff'
            this.optionFinishChart.legend.textStyle.color = '#fff'
          }
          this.optionFinishChart.yAxis.max = Math.ceil(maxVal / Number(str)) * str
          this.optionFinishChart.xAxis.data = arr[2].equip_data
          this.optionFinishChart.series[0].data = plan_actual_actual_trains
          this.optionFinishChart.series[1].data = plan_actual_diff_trains
          this.optionFinishChart.series[2].data = plan_actual_plan_trains

          this.myChartFinishChart.setOption(this.optionFinishChart)
        }

        if (!bool1 && !bool2) {
          // 第一个数据 第一个图
          const plan_actual_data_plan_trains = this.setVal(arr[1].plan_actual_data, 'plan_trains')
          const plan_actual_data_actual_trains = this.setVal(arr[1].plan_actual_data, 'actual_trains')
          const plan_add_sulfur_trains = this.setVal(arr[1].plan_actual_data, 'plan_add_sulfur_trains')
          const plan_without_sulfur_trains = this.setVal(arr[1].plan_actual_data, 'plan_without_sulfur_trains')
          const actual_add_sulfur_trains = this.setVal(arr[1].plan_actual_data, 'actual_add_sulfur_trains')
          const actual_without_sulfur_trains = this.setVal(arr[1].plan_actual_data, 'actual_without_sulfur_trains')
          this.optionYieldBar.xAxis.data = arr[1].date_range
          this.optionYieldBar.series[0].data = plan_actual_data_plan_trains
          this.optionYieldBar.series[3].data = plan_actual_data_actual_trains
          this.optionYieldBar.series[1].data = plan_add_sulfur_trains
          this.optionYieldBar.series[2].data = plan_without_sulfur_trains
          this.optionYieldBar.series[4].data = actual_add_sulfur_trains
          this.optionYieldBar.series[5].data = actual_without_sulfur_trains
          if (this.bigScreen) {
            this.optionYieldBar.xAxis.axisLine.lineStyle.color = '#fff'
            this.optionYieldBar.yAxis.axisLine.lineStyle.color = '#fff'
            this.optionYieldBar.title.textStyle.color = '#fff'
            this.optionYieldBar.legend.textStyle.color = '#fff'
            this.optionYieldBar.series[0].itemStyle.normal.label.color = '#fff'
          }
          this.myChartYieldBar.setOption(this.optionYieldBar)
        }
        if (!bool && !bool1) {
          // 第四个数据
          const maintenance_data_minutes = this.setVal(arr[3].maintenance_data, 'minutes')
          this.optionShutdownBar.series[0].data = maintenance_data_minutes
          this.optionShutdownBar.xAxis.data = arr[3].equip_data
          if (this.bigScreen) {
            this.optionShutdownBar.xAxis.axisLine.lineStyle.color = '#fff'
            this.optionShutdownBar.yAxis.axisLine.lineStyle.color = '#fff'
            this.optionShutdownBar.title.textStyle.color = '#fff'
            this.optionShutdownBar.series[0].itemStyle.normal.label.color = '#fff'
          }
          this.myChartShutdownBar.setOption(this.optionShutdownBar)
        }
      } catch (e) {
        //
      }
    },
    handleClick(str) {
      this[str].dateFinish = []
      this[str].st = ''
      this[str].et = ''
      if (str === 'equipMaintenance') {
        this.getList(false, false, true)
      } else {
        this.getList(false, true, false)
      }
    },
    handleClickDate(val, str) {
      if (val) {
        this[str].dimension = ''
        this[str].st = val[0]
        this[str].et = val[1]
      } else {
        this[str].st = ''
        this[str].et = ''
        this[str].dimension = '1'
      }
      if (str === 'equipMaintenance') {
        this.getList(false, false, true)
      } else {
        this.getList(false, true, false)
      }
    },
    setVal(a, b, bool) {
      const c = []
      for (const key in a) {
        if (Object.hasOwnProperty.call(a, key)) {
          const element = a[key]
          if (element[b] === 0 && bool) {
            element[b] = ''
          }
          c.push(element[b])
        }
      }
      return c
    },
    yieldBarChange(val) {
      this.getList(true)
    }
  }
}
</script>

<style lang="scss">
.homePage-container {
  // background-color: #f0f2f5;
  padding:0 20px;
  .yieldBar{
    position: relative;
  }
  .yieldBarRadio{
    position: absolute;
    top:13px;
    right:20px;
    z-index: 100;
  }
  .yieldBarLine{
      position: absolute;
    top:13px;
    right:20px;
    z-index: 100;
  }
  .volumeBox{
    background: #fff;
    // padding:10px;
    border-radius: 20px;
    margin-bottom:10px;
  }
  .volumeBoxChild{
    text-align:center;
    font-size:25px;
    padding: 6px 0;
  }
  .homePage-title{
    width:100%;
    text-align: center;
    padding: 10px;
  }
  .homePage-status{
    display: flex;
  }
  .status-left{
    flex:1;
  }
  .status-right{
    width:0px;
  }
  .status-left{
    display: flex;
  }
  .status-num{
    text-align: center;
    width:160px;
    font-size:18px;
  }
  .status-circular-circular{
    width:40%;
  }
  .status-circular-line{
    width:80%;
    margin-right: 80px;
  }
  .status-circular{
    flex:1
  }
  .el-col{
    margin-top:10px;
  }
  .relativeFa{
    position: relative;
  }
  .absoluteFa{
    position: absolute;
    top:0;right:0px;
    display: flex;
  }
}
.bigScreen{
  min-height: 100vh;
 background-image: url(../../assets/pageBg.f9f9dcd5.png);
 .el-row{
   padding-top:20px;
 }
  .set-current-time{
    font-size:20px !important;
  }
 .el-card{
   background: transparent !important;
   border: 2px solid rgb(24 122 174 / 70%);
 }
 .volumeBoxChild{
   padding: 10px 0;
   color:#fff !important;
 }
 .volumeBox{
   background: transparent !important;
   height: 360px!important;
 }
 .el-input__inner{
   background: transparent !important;
 }
.el-date-editor .el-range-input{
   background: transparent !important;
 }
 .el-tabs__item,.el-date-editor .el-range-input{
   color:#fff;
 }
   .head-top{
    display: flex;
    justify-content: space-between ;
     align-items: center;
     color:#fff;
  }
    .d-flex{
      margin-top: 10px;
    display: flex;
    h2{
      margin:15px;
    }
    .decoration10{
      width:480px;
      height: 3px;
      background:rgb(74, 107, 178);
      box-shadow: 0 2px 12px 0 rgb(74, 107, 178);
    }
    .decoration8{
      transform: rotate(60deg);
      margin-top:40px;
      height: 3px;
      width:86px;
      background:rgb(74, 107, 178);
      margin-left:-20px;
      margin-right:-20px;
      box-shadow: 0 2px 12px 0 rgb(74, 107, 178);
    }
    .decoration8-1{
       transform: rotate(120deg)
    }
    .title{
      padding-bottom:17px;
      position: relative;
      margin-bottom:10px ;
    }
    .title-border{
      position: absolute;
      bottom:0;
      width:100%;
      height: 3px;
      background:rgb(74, 107, 178);
      box-shadow: 0 2px 12px 0 rgb(74, 107, 178);
    }
  }
}

</style>
