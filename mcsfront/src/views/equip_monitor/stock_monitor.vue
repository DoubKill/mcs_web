<template>
  <div v-loading="loading">
    <!-- 在制库存监控 -->
    <div
      id="taskLine"
      style="width: 95%;height:750px"
    />
  </div>
</template>

<script>
import { stockMonitor } from '@/api/jqy'
import * as echarts from 'echarts'
export default {
  name: 'StockMonitor',
  components: { },
  data() {
    return {
      getParams: {},
      loading: false,
      option: {
        color: ['#59A0F7', '#71C87C'],
        title: {
          left: 'center',
          text: '各工序在制库存'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          top: '6%',
          orient: 'horizontal',
          data: ['缓存站', 'AGV小车']
        },
        toolbox: {
          show: true
        },
        calculable: true,
        grid: {
          x: 60,
          y: 100,
          x2: 0,
          y2: 30
        },
        xAxis: [
          {
            type: 'category',
            // prettier-ignore
            data: []
          }
        ],
        yAxis: [
          {
            name: '库存量(篮)',
            type: 'value'
          }
        ],
        series: [
          {
            barGap: '0%',
            name: '缓存站',
            type: 'bar',
            data: [],
            label: {
              color: '#000000',
              position: 'top',
              show: true,
              formatter: function(params) {
                if (params.value === 0 || params.value === '0') {
                  return ''
                } else {
                  return params.value
                }
              }
            }
          },
          {
            barGap: '0%',
            name: 'AGV小车',
            type: 'bar',
            data: [],
            label: {
              color: '#000000',
              position: 'top',
              show: true,
              formatter: function(params) {
                if (params.value === 0 || params.value === '0') {
                  return ''
                } else {
                  return params.value
                }
              }
            }
          }
        ]
      }
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/stock-monitor') {
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
          }, 5000)
        } else {
          window.clearInterval(this._setInterval)
        }
      },
      deep: true, // 深度监听
      immediate: true // 第一次初始化渲染就可以监听到
    }
  },
  created() {
    // this.getList()
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await stockMonitor('get', null, { params: this.getParams })
        this.option.xAxis[0].data = data.data.processes
        this.option.series[0].data = data.data.stations
        this.option.series[1].data = data.data.agv
        this.$nextTick(() => {
          const chartBar = echarts.init(document.getElementById('taskLine'))
          chartBar.setOption(this.option)
        })
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss">

</style>
