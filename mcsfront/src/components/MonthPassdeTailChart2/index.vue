<template>
  <el-row>
    <el-col :xs="24" :sm="24" :md="24" :lg="24">
      <div id="dialogRateBar" style="width: 100%; height: 400px" />
    </el-col>
  </el-row>
</template>

<script>
import echarts from 'echarts'

export default {
  props: {
    dataList: {
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
    }
  },
  data() {
    return {
      option: {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          },
          formatter: (params) => { return this.formatterFun(params) },
          extraCssText: 'white-space: normal; word-break: break-all;'
        },
        grid: {
          top: '12%',
          left: '5%',
          right: '8%',
          containLabel: true
        },
        dataZoom: [
          {
            show: true,
            start: 90,
            end: 100
          }
        ],
        // dataset: {
        //   source: [['一次', '流变', '综合']]
        // },
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
            name: '合格率'
          }
        ],
        series: []
      }
    }
  },
  watch: {
    dataList(val) {
      if (val) {
        this.drawLine()
      }
    }
  },
  created() {
  },
  mounted() {
    this.$nextTick(function() {
      this.drawLine()
    })
  },
  methods: {
    formatterFun(params) {
      if (params instanceof Array) {
        let str = ''
        str += `${params[0].axisValue}<br/>`
        params.forEach((m, index) => {
          str += `<span class="chart-tooltip-color" style="display: inline-block; margin-right: 10px; background-color: ${m.color}; width: 10px; height: 10px; border-radius:100%; margin-right: 5px"></span>`
          str += `${m.seriesName}：${m.data}`
          str += `${index % 6 === 0 ? '<br/>' : '     '}` // 一排放几个可根据实际情况改变
        })
        return str
      }
    },
    drawLine() {
      const headers2 = []
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
      this.headers.equips.forEach(D => {
        const _arr1 = []
        const _arr2 = []
        const _arr3 = []
        this.dataList.forEach(d => {
          const a1 = d.equips.filter(d1 => d1.production_equip_no === D)
          if (a1.length > 0) {
            _arr1.push(a1[0].yc_percent_of_pass ? a1[0].yc_percent_of_pass.replace(/%/g, '') : '')
            _arr2.push(a1[0].lb_percent_of_pass ? a1[0].lb_percent_of_pass.replace(/%/g, '') : '')
            _arr3.push(a1[0].zh_percent_of_pass ? a1[0].zh_percent_of_pass.replace(/%/g, '') : '')
          } else {
            _arr1.push(0)
            _arr2.push(0)
            _arr3.push(0)
          }
        })
        arr1.push({
          name: D + '一次',
          value: D,
          type: 'bar',
          data: _arr1
        })
        arr1.push({
          name: D + '流变',
          value: D,
          type: 'bar',
          data: _arr2
        })
        arr1.push({
          name: D + '综合',
          value: D,
          type: 'bar',
          data: _arr3
        })
      })
      const arr2 = []
      this.headers.classes.forEach(D => {
        const _arr1 = []
        const _arr2 = []
        const _arr3 = []
        this.dataList.forEach(d => {
          const a1 = d.classes.filter(d1 => d1.production_class === D)
          if (a1.length > 0) {
            _arr1.push(a1[0].yc_percent_of_pass ? a1[0].yc_percent_of_pass.replace(/%/g, '') : '')
            _arr2.push(a1[0].lb_percent_of_pass ? a1[0].lb_percent_of_pass.replace(/%/g, '') : '')
            _arr3.push(a1[0].zh_percent_of_pass ? a1[0].zh_percent_of_pass.replace(/%/g, '') : '')
          } else {
            _arr1.push(0)
            _arr2.push(0)
            _arr3.push(0)
          }
        })
        arr1.push({
          name: D + '一次',
          value: D,
          type: 'bar',
          data: _arr1
        })
        arr1.push({
          name: D + '流变',
          value: D,
          type: 'bar',
          data: _arr2
        })
        arr1.push({
          name: D + '综合',
          value: D,
          type: 'bar',
          data: _arr3
        })
      })
      this.dataList.forEach(D => {
        headers2.push(D.date)
        obj2.data.push(D.yc_percent_of_pass ? D.yc_percent_of_pass.replace(/%/g, '') : '')
        obj3.data.push(D.lb_percent_of_pass ? D.lb_percent_of_pass.replace(/%/g, '') : '')
        obj4.data.push(D.zh_percent_of_pass ? D.zh_percent_of_pass.replace(/%/g, '') : '')
      })

      // 图表初始化
      this.$nextTick(() => {
        this.chartDialogRateBar = echarts.init(document.getElementById('dialogRateBar'))
        const allArr = [obj2, obj3, obj4, ...arr1, ...arr2]
        this.option.xAxis[0].data = headers2
        this.option.series = allArr
        this.chartDialogRateBar.setOption(this.option)
      })
    }
  }
}
</script>
