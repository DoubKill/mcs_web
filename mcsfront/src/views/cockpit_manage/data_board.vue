<template>
  <div style="padding:5px">
    <!-- 数据看板 -->
    <el-row :gutter="20">
      <el-col :span="5"><div class="grid-content bg-purple">
        <el-card shadow="always">
          <h3 style="display: inline-block;margin-right: 8px;">AGV利用详情</h3>
          <!-- <el-select v-model="value" size="mini" clearable placeholder="请选择">
            <el-option
              v-for="item in []"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select> -->
          <div
            id="doughnutChart"
            style="width: 100%;height:350px;"
          />
        </el-card>
      </div></el-col>
      <el-col :span="9"><div class="grid-content bg-purple">
        <el-card shadow="always">
          <h3 style="display: inline-block;margin-right: 8px;">各工序在制库存</h3>
          <div
            id="barChart"
            style="width: 100%;height:350px;"
          />
        </el-card>
      </div></el-col>
      <el-col :span="7"><div class="grid-content bg-purple">
        <el-card shadow="always" :body-style="{ padding: '0px' }">
          <div style="background:#3aa7e6">
            <h3 style="display: inline-block;margin: 25px 0 20px 8px;color:#fff;margin-left:10px">总产能趋势</h3>
            <div
              id="capacityLineChart"
              style="width: 100%;height:293px;"
            />
          </div>
          <div style="padding: 14px;padding-top: 0px;">
            <div class="bottom clearfix w_flex">
              <div style="text-align:center">
                <h3 style="margin-top:0">{{ yesterdayTotal }}(万片)</h3>
                昨日产出
              </div>
              <div style="border-right:1px solid #cbbebf" />
              <div style="text-align:center">
                <h3 style="margin-top:0">{{ todayTotal }}(万片)</h3>
                今日产出
              </div>
            </div>
          </div>
        </el-card>
      </div></el-col>
      <el-col :span="3"><div class="grid-content bg-purple">
        <el-card shadow="always">
          <h3 style="display: inline-block;margin-right: 8px;">站台预警</h3>
          <div style="width: 100%;height:350px;padding:20px">
            <h2>站台堆料预警</h2>
            <h1 :style="{'color':w_color[2]}">{{ stow_alarm }}</h1>
            <h2>站台缺料预警</h2>
            <h1 :style="{'color':w_color[0]}">{{ short_alarm }}</h1>
          </div>
        </el-card>
      </div></el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top:15px">
      <el-col :span="16">
        <el-card shadow="always">
          <h3 style="display: inline-block;margin-right: 8px;">今日工序产量</h3>
          <div
            id="processLineChart"
            style="width: 100%;height:300px;"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="always" :body-style="{ padding: '0px' }">
          <h3 style="display: inline-block;padding-right: 8px;background: #3aa7e6;" class="titleColor">缓存站占比TOP10</h3>
          <el-table
            :data="tableData"
            style="width: 100%"
            height="315px"
          >
            <el-table-column
              prop="date"
              label="序号"
              width="80"
            >
              <template slot-scope="{$index}">
                <div :style="{'background':$index<3?'rgb(58, 167, 230)':'','color':$index<3?'#fff':'#000'}" class="snStyle">{{ $index+1 }}</div>
              </template>
            </el-table-column>
            <el-table-column
              prop="equip_name"
              label="设备名称"
              width="150"
            />
            <el-table-column
              prop="address"
              label="占用比例"
            >
              <template slot-scope="{row}">
                <el-progress :percentage="row.ratio" />
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import * as echarts from 'echarts'
import { dataBoard } from '@/api/base_w'
import { stockMonitor } from '@/api/jqy'
export default {
  name: 'DataBoard',
  data() {
    return {
      value: '',
      w_color: ['#6699FF', '#66CCCC', '#66CC33', '#FFCC33', '#ff6e76', '#05c091', '#CCCC66', '#FF6699', '#66FF99', '#669933', '#6600FF', '#33CCCC'],
      optionDoughnut: {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: 'bottom',
          left: 'center'
        },
        series: [
          {
            name: 'agv利用率',
            type: 'pie',
            radius: ['50%', '70%'],
            center: ['50%', '45%'],
            avoidLabelOverlap: false,
            label: {
              show: true,
              formatter(param) {
                return param.name + param.percent + '%' + '\n (' + param.value + ')'
              }
            },
            labelLine: {
              show: true
            },
            emphasis: {
              label: {
                show: true
              }
            },
            data: []
          }
        ]
      },
      optionbar: {
        legend: {
          top: 'bottom',
          left: 'center'
        },
        grid: {
          left: '5%',
          right: '3%',
          top: '3%',
          bottom: '11%',
          containLabel: true
        },
        tooltip: {},
        xAxis: { type: 'category', data: [],
          axisLabel: {
            interval: 0 // 坐标轴刻度标签的显示间隔
            // rotate: 40 // 标签倾斜的角度
          }},
        yAxis: { name: '库存量(篮)',
          nameGap: '25',
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#a0a0a0',
            fontSize: 16,
            padding: 3
          }},
        series: [
          {
            name: '缓存站',
            type: 'bar',
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: 'AGV小车',
            type: 'bar',
            data: [220, 182, 191, 234, 290, 330, 310]
          }
        ]
      },
      optionCapacityLine: {
        color: ['#fff', '#d6d841f2'],
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['今天', '昨天'],
          textStyle: {
            color: '#fff'
          },
          top: 'bottom',
          left: 'center'
        },
        grid: {
          left: '8%',
          right: '4%',
          top: '3%',
          bottom: '11%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          nameGap: '25',
          name: '产量(百片)',
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#fff',
            fontSize: 16,
            padding: 10
          }
        },
        series: [
          {
            name: '今天',
            type: 'line',
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: '昨天',
            type: 'line',
            data: [220, 182, 191, 234, 290, 330, 310]
          }
        ]
      },
      optionProcessLine: {
        tooltip: {
          trigger: 'axis',
          position: function(point, params, dom, rect, size) {
            if ((size.viewSize[0] / 2) >= point[0]) {
              return [point[0], '8%']
            } else {
              return [point[0] - 100, '8%']
            }
          }
        },
        legend: {
          data: ['今天', '昨天'],
          top: 'bottom',
          left: 'center'
        },
        grid: {
          left: '4%',
          right: '3%',
          top: '3%',
          bottom: '12%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value',
          nameGap: '35',
          name: '产量(百片)',
          nameLocation: 'middle'
        },
        series: [
          {
            name: '今天',
            type: 'line',
            data: []
          },
          {
            name: '昨天',
            type: 'line',
            data: []
          }
        ]
      },
      tableData: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
      stow_alarm: '',
      short_alarm: '',
      yesterdayTotal: '',
      todayTotal: ''
    }
  },
  mounted() {
    this.optionbar.color = this.w_color
    this.optionDoughnut.color = this.w_color
    this.optionProcessLine.color = this.w_color

    this.doughnutChart = echarts.init(document.getElementById('doughnutChart'))

    this.barChart = echarts.init(document.getElementById('barChart'))

    this.capacityLineChart = echarts.init(document.getElementById('capacityLineChart'))

    this.processLineChart = echarts.init(document.getElementById('processLineChart'))
  },
  created() {
    this.getList()
  },
  methods: {
    async getList(type) {
      try {
        this.loading = true
        const data = await dataBoard('get', null, { params: { }})
        const data1 = await stockMonitor('get', null, { params: {}})
        this.optionbar.xAxis.data = data1.data.processes
        this.optionbar.series[0].data = data1.data.stations
        this.optionbar.series[1].data = data1.data.agv
        this.barChart.setOption(this.optionbar, true)

        this.stow_alarm = data.stow_alarm
        this.short_alarm = data.short_alarm

        this.optionDoughnut.series[0].data = data.agv_status
        this.doughnutChart.setOption(this.optionDoughnut, true)

        let sum = 0
        let sum1 = 0
        data.丝网_old.reduce(function(pre, curr) {
          sum = pre + curr
          return sum
        })
        data.丝网.reduce(function(pre, curr) {
          sum1 = pre + curr
          return sum1
        })
        this.yesterdayTotal = (sum / 100).toFixed(0)
        this.todayTotal = (sum1 / 100).toFixed(0)
        this.optionCapacityLine.series[0].data = data.丝网_old
        this.optionCapacityLine.series[1].data = data.丝网
        this.optionCapacityLine.xAxis.data = data.axis
        this.capacityLineChart.setOption(this.optionCapacityLine, true)

        this.optionProcessLine.xAxis.data = data.axis
        this.optionProcessLine.legend.data = data.processes
        this.optionProcessLine.series = []
        data.processes.forEach((d, i) => {
          if (data[d]) {
            this.optionProcessLine.series[i] = {
              name: d,
              type: 'line',
              data: []
            }
            this.optionProcessLine.series[i].data = data[d]
          }
        })
        this.processLineChart.setOption(this.optionProcessLine, true)

        this.tableData = data.stock_top10

        this.loading = false
      } catch (e) {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
    .w_flex{
        display: flex;
        justify-content: space-between;
    }
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }
  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }

  .clearfix:after {
      clear: both
  }

  .titleColor{
    background: rgb(58, 167, 230);
    padding-right: 8px;
    margin: 0;
    padding: 20px;
    width: 100%;
    color: #fff;
  }
  .snStyle{
    color: #fff;
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 10px;
    text-align: center;
    line-height: 20px;
  }
</style>
