<template>
  <div class="QTime_forms">
    <!-- 堆栈超时料报表 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <el-table :data="tableData" stripe style="width: 80%">
        <el-table-column label="属性名称" prop="equip_code">
          <!-- <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.desc" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column> -->
          <template slot-scope="{row}">
            {{ row.equip_code }}
          </template>
        </el-table-column>
        <el-table-column label="超时物料" prop="expire_basket">
          <!-- <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.desc" size="small" clearable @input="getList" />
            </template>
          </el-table-column> -->
          <template slot-scope="{row}">
            {{ row.expire_basket }}
          </template>
        </el-table-column>
        <el-table-column label="总物料" prop="total_basket">
          <!-- <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.desc" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column> -->
          <template slot-scope="{row}">
            {{ row.total_basket }}
          </template>
        </el-table-column>
        <el-table-column label="超时比例" prop="expire_ratio">
          <!-- <el-table-column min-width="10">
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column> -->
          <template slot-scope="{row}">
            {{ row.expire_ratio }}
          </template>
        </el-table-column>
      </el-table>

      <div id="QTimeBar" style="width: 80%;height:400px;margin-top:10px" />
    </div>
  </div>
</template>

<script>
import echarts from 'echarts'
import { qtimeReport } from '@/api/base_w'
export default {
  name: 'QTimeForms',
  data() {
    return {
      tableData: [],
      getParams: {},
      loading: false,
      option: {
        title: {
          text: '暂存超时料',
          left: 'center'
        },
        legend: {
          data: ['未超时物料', '超时物料'],
          bottom: '0%'
        },
        xAxis: {
          data: [1, 2, 3, 4],
          name: '',
          axisLine: { onZero: true },
          splitLine: { show: false },
          splitArea: { show: false }
        },
        yAxis: {
          type: 'value', axisLabel: {
            formatter: '{value} %'
          },
          max: 100
        },
        grid: {
          bottom: 50
        },
        series: [
          {
            name: '未超时物料',
            type: 'bar',
            stack: '11',
            barMaxWidth: 150,
            label: {
              show: false,
              color: '#fff'
            },
            data: ['', 2, 3, 4],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 1, color: 'green' }
            ])
          },
          {
            name: '超时物料',
            type: 'bar',
            stack: '11',
            barMaxWidth: 150,
            label: {
              normal: {
                show: false,
                color: '#fff'
              }
            },
            data: [1, 6, 7, 8],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 1, color: 'red' }
            ])
          }
        ]
      },
    }
  },
  created() {
  },
  mounted() {
    this.QTimeBar = echarts.init(document.getElementById('QTimeBar'))
    this.QTimeBar.setOption(this.option, true)

    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        this.tableData = []
        const data = await qtimeReport('get', null, { params: {} })
        this.tableData = data || []

        let arr = []
        let arr1 = []  //未超时物料
        let arr2 = []  //超时物料
        this.tableData.forEach(d=>{
          arr.push(d.equip_code)
          arr1.push(d.effective_ratio)
          arr2.push(d.expire_ratio)
        })
        this.option.xAxis.data = arr
        this.option.series[0].data = arr1
        this.option.series[1].data = arr2
        this.QTimeBar.setOption(this.option)
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
  }
}
</script>

<style lang="scss">
  //  .QTime_forms .el-table__body-wrapper{
  //     height: auto !important;
  //   }
</style>