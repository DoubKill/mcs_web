<template>
  <el-row>
    <el-col :xs="24" :sm="24" :md="24" :lg="24">
      <div id="dialogRateBar1" style="width: 100%;height:400px" />
    </el-col>
  </el-row>

</template>

<script>
import echarts from 'echarts'
import dayjs from 'dayjs'
export default {
  props: {
    chartsdata: {
      type: Array,
      default() {
        return {}
      }
    },
    headers: {
      type: Object,
      default() {
        return {}
      }
    },
    comprehensiveBarShow: {
      type: Boolean
    }
  },
  data() {
    return {
      option: {
        legend: {
          data: ['产量', '一次合格率%', '流变合格率%', '综合合格率%']
        },
        tooltip: {
          trigger: 'axis',
          confine: true,
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        grid: {
          top: '12%',
          left: '5%',
          right: '8%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            name: '月份',
            data: []
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: '合格率',
            axisLabel: {
              formatter: '{value} %'
            }
          },
          {
            type: 'value',
            name: '产量',
            axisLabel: {
              formatter: '{value}'
            }
          },
          {
            type: 'value',
            name: '数量',
            offset: 80,
            axisLabel: {
              formatter: '{value}'
            }
          }
          // {
          //   type: 'value',
          //   name: '合格率%/数量'
          // }
        ],
        dataZoom: [
          {
            show: true,
            start: 0,
            end: 100
          }
        ],
        series: []
      }
    }
  },
  watch: {
    comprehensiveBarShow(val) {
      if (val) {
        this.drawLine()
      }
    }
  },
  created() {
    // console.log('this.option', this.option)
  },
  mounted() {
    // this.$nextTick(function() {
    this.drawLine()
    // })
    // this.drawLine()
  },
  methods: {
    drawLine() {
      const headers2 = []
      const obj1 = {
        name: '产量',
        type: 'line',
        yAxisIndex: 1,
        data: []
      }
      const obj2 = {
        name: '一次合格率%',
        type: 'bar',
        data: []
      }
      const obj3 = {
        name: '流变合格率%',
        type: 'bar',
        data: []
      }
      const obj4 = {
        name: '综合合格率%',
        type: 'bar',
        data: []
      }
      const arr1 = []
      this.headers.points.forEach(D => {
        const _arr1 = []
        const _arr2 = []
        const _arr3 = []
        const _arr4 = []
        this.chartsdata.forEach(d => {
          const a1 = d.points.filter(d1 => d1.name === D)
          if (a1.length > 0) {
            _arr1.push(a1[0].upper_limit_percent ? a1[0].upper_limit_percent.replace(/%/g, '') : '')
            _arr2.push(a1[0].lower_limit_percent ? a1[0].lower_limit_percent.replace(/%/g, '') : '')
            _arr3.push(a1[0].upper_limit_count)
            _arr4.push(a1[0].lower_limit_count)
          } else {
            _arr1.push(0)
            _arr2.push(0)
            _arr3.push(0)
            _arr4.push(0)
          }
        })
        arr1.push({
          name: D + '% +',
          value: D,
          type: 'bar',
          data: _arr1
        })
        arr1.push({
          name: D + '% -',
          value: D,
          type: 'bar',
          data: _arr2
        })
        arr1.push({
          name: D + '+',
          value: D,
          type: 'line',
          yAxisIndex: 2,
          data: _arr3
        })
        arr1.push({
          name: D + '-',
          value: D,
          yAxisIndex: 2,
          type: 'line',
          data: _arr4
        })
      })
      this.chartsdata.forEach(D => {
        headers2.push(dayjs(D.date).format('YYYY-MM'))
        obj1.data.push(D.train_count)
        obj2.data.push(D.yc_percent_of_pass ? D.yc_percent_of_pass.replace(/%/g, '') : '')
        obj3.data.push(D.lb_percent_of_pass ? D.lb_percent_of_pass.replace(/%/g, '') : '')
        obj4.data.push(D.zh_percent_of_pass ? D.zh_percent_of_pass.replace(/%/g, '') : '')
      })

      this.$nextTick(() => {
        this.chartDialogRateBar = echarts.init(document.getElementById('dialogRateBar1'))
        const allArr = [obj1, obj2, obj3, obj4, ...arr1]
        this.option.xAxis[0].data = headers2
        this.option.series = allArr
        this.chartDialogRateBar.setOption(this.option)
      })
    }
  }
}
</script>
<style scoped lang='less'>

</style>
