<template>
  <div>
    <!-- 统计看板 -->
    <el-card shadow="always">
      <h3 style="display: inline-block;margin-right: 8px;">异常任务比例统计</h3>
      <div>
        <div
          id="barChartTop"
          style="width: 50%;height:350px;display: inline-block;"
        />
        <div
          id="lineChartTop"
          style="width: 50%;height:350px;display: inline-block;"
        />
      </div>
    </el-card>
  </div>
</template>
<script>
import * as echarts from 'echarts'
export default {
  name: 'StatisticalKanban',
  data() {
    return {
      w_color: ['#6699FF', '#66CCCC', '#66CC33', '#FFCC33', '#ff6e76', '#05c091'],
      optionBarTop: {},
      optionlineTop: {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['今天', '昨天'],
          top: 'bottom',
          left: 'center',
          show: false
        },
        grid: {
          left: '2%',
          right: '7%',
          top: '3%',
          bottom: '12%'
        //   containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisLine: {
            show: true,
            lineStyle: {
              color: '#EBEBEB'
            }
          },
          nameTextStyle: {
            color: '#797979'
          },
          axisLabel: {
            color: '#797979'
          },
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value',
          nameGap: '35',
          nameLocation: 'middle',
          position: 'right',
          axisLine: {
            show: true,
            lineStyle: {
              color: '#EBEBEB'
            }
          },
          nameTextStyle: {
            color: '#797979'
          },
          axisLabel: {
            color: '#797979'
          }
        },
        series: [
          {
            name: '今天',
            type: 'line',
            data: [120, 132, 101, 134, 90, 230, 210]
          }
        ]
      }
    }
  },
  mounted() {
    const legenddata = ['月', '周']
    const xAxis = []
    const xAxisList = ['M9', 'M10', 'M11', 'W46', 'W47']
    const xAxisitem = {
      type: 'category',
      data: '',
      position: 'bottom',
      axisTick: {
        show: false
      },
      axisLine: {
        show: true,
        lineStyle: {
          color: '#EBEBEB'
        }
      },
      nameTextStyle: {
        color: '#797979'
      },
      axisLabel: {
        color: '#797979'
      }
    }
    let xAxisitemdata = []
    for (let i = 0; i < xAxisList.length; i++) {
      xAxisitemdata = []
      for (let i = 0; i < xAxisList.length; i++) {
        xAxisitemdata.push('')
      }
      xAxisitemdata[i] = xAxisList[i]
      xAxisitem.data = JSON.parse(JSON.stringify(xAxisitemdata))
      xAxis.push(JSON.parse(JSON.stringify(xAxisitem)))
    }
    console.log('xAxis', xAxis)
    const series = []

    const arr = ['0.65', '0.73', '0.7', '0.72', '0.57']
    arr.forEach((d, i) => {
      const _data = []
      for (let a = 0; a < i; a++) {
        _data.push('')
      }
      _data.push(d)
      const seriesitem = {
        type: 'bar',
        name: i < 3 ? legenddata[0] : legenddata[1],
        barWidth: '70',
        xAxisIndex: i,
        data: _data
      }
      const aa = JSON.parse(JSON.stringify(seriesitem))
      aa.label = {
        show: true,
        position: 'top',
        formatter: (val) => {
          return `${val}%`
        }
      }
      series.push(aa)
    })
    console.log('series', series)
    const series1 = JSON.parse(JSON.stringify(series))

    const option = {
      color: this.w_color,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          var html = ''
          if (params.length !== 0) {
            var getName = params[0].name
            html += getName + '<br/>'
            for (var i = 0; i < params.length; i++) {
              if (
                params[i].value != null &&
                                    params[i].value !== 0 &&
                                    params[i].value !== ''
              ) {
                html += params[i].marker
                html += params[i].seriesName + ': ' + params[i].value + '%' + '<br/>'
              }
            }
          }
          return html
        }
      },
      legend: {
        itemHeight: 13,
        data: legenddata,
        top: 'bottom',
        left: 'center',
        textStyle: {
          fontSize: 14,
          height: 10,
          rich: {
            a: {
              verticalAlign: 'middle'
            }
          }
        }
      },
      grid: {
        left: '5%',
        right: '0%',
        top: '3%',
        bottom: '12%'
        // containLabel: true
      },
      xAxis: xAxis,
      yAxis: [
        {
          type: 'value',
          splitLine: {
            show: false
          },
          name: '异常任务比例%',
          axisLine: {
            show: true,
            lineStyle: {
              color: '#EBEBEB'
            }
          },
          nameTextStyle: {
            color: '#797979'
          },
          axisLabel: {
            color: '#797979'
          }
        }
      ],
      series: series1
    }

    this.barChartTop = echarts.init(document.getElementById('barChartTop'))
    // this.barChartTop.setOption(this.optionBarTop, true)
    this.barChartTop.setOption(option)

    this.optionlineTop.color = this.w_color
    this.lineChartTop = echarts.init(document.getElementById('lineChartTop'))
    this.lineChartTop.setOption(this.optionlineTop, true)
  },
  methods: {
    name() {

    }
  }
}
</script>

<style lang="scss" scoped>

</style>
