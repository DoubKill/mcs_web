<template>
  <div>
    <!-- 数据显示 -->
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="always">
          <div
            id="barChartTop"
            style="width: 100%;height:350px;display: inline-block;"
          />
        </el-card>
        <el-card shadow="always" style="margin-top:20px">
          <div
            id="barChartBottom"
            style="width: 100%;height:350px;display: inline-block;"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="always">
          <div
            id="barChartMiddel"
            style="width: 100%;height:800px;display: inline-block;"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-table
          :data="tableData"
          stripe
          border
          style="width: 100%"
          height="350px"
        >
          <el-table-column
            prop="date"
            label="日期"
            width="180"
          />
          <el-table-column
            prop="name"
            label="姓名"
            width="180"
          />
          <el-table-column
            prop="address"
            label="地址"
          />
        </el-table>

        <el-row :gutter="20">
          <el-col :span="16">
            <el-card shadow="always">
              <h3 style="margin-right: 8px;">任务达成率</h3>
              <h4 style="display:inline-block;">站台堆料预警：</h4>
              <h4 style="display:inline-block" :style="{'color':w_color[2]}">5</h4>
              <h4 style="display:inline-block;margin-left:10px">站台缺料预警：</h4>
              <h4 style="display:inline-block" :style="{'color':w_color[0]}">5</h4><br>
              <h4 style="display:inline-block;">站台堆料预警：</h4>
              <h4 style="display:inline-block" :style="{'color':w_color[2]}">5</h4>
              <h4 style="display:inline-block;margin-left:10px">站台缺料预警：</h4>
              <h4 style="display:inline-block" :style="{'color':w_color[0]}">5</h4>

              <h2 style="margin-right: 8px;">站台异常TOP10</h2>
              <el-table
                :data="tableData1"
                style="width: 100%"
                height="315px"
              >
                <el-table-column
                  prop="date"
                  label="序号"
                >
                  <template slot-scope="{$index}">
                    <div :style="{'background':$index<3?'rgb(58, 167, 230)':'','color':$index<3?'#fff':'#000'}" class="snStyle">{{ $index+1 }}</div>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="设备名称"
                />
                <el-table-column
                  prop="name"
                  label="设备名称"
                />
                <el-table-column
                  prop="address"
                  label="占用比例"
                />
              </el-table>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="always">
              <h3 style="display: inline-block;margin-right: 8px;">站台预警</h3>
              <div style="width: 100%;height:400px;padding:20px">
                <h2>站台堆料预警</h2>
                <h1 :style="{'color':w_color[2]}">5</h1>
                <h2>站台缺料预警</h2>
                <h1 :style="{'color':w_color[0]}">5</h1>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import * as echarts from 'echarts'
export default {
  name: 'DataDisplay',
  data() {
    return {
      w_color: ['#6699FF', '#66CCCC', '#66CC33', '#FFCC33', '#ff6e76', '#05c091'],
      optionBarTop: {
        title: {
          text: '累计产出（万片）'
        },
        legend: {},
        grid: {
          left: '2%',
          right: '4%',
          top: '13%',
          bottom: '3%',
          containLabel: true
        },
        tooltip: {},
        xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
        yAxis: { },
        series: [
          {
            name: 'Mon',
            type: 'bar',
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: 'Tue',
            type: 'bar',
            data: [220, 182, 191, 234, 290, 330, 310]
          }
        ]
      },
      optionBarBottom: {
        title: {
          text: '在制（车）'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {},
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            axisLabel: { interval: 0, rotate: 30 }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: 'Email',
            type: 'bar',
            stack: 'Ad',
            emphasis: {
              focus: 'series'
            },
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: 'Union Ads',
            type: 'bar',
            stack: 'Ad',
            emphasis: {
              focus: 'series'
            },
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: 'Video Ads',
            type: 'bar',
            stack: 'Ad',
            emphasis: {
              focus: 'series'
            },
            data: [150, 232, 201, 154, 190, 330, 410]
          }
        ]
      },
      optionBarMiddel: {
        title: {
          text: '丝网累计产出（万片）'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01],
          min: 0,
          axisTick: {
            show: false // 刻度线
          },
          axisLine: {
            show: false // 隐藏y轴
          },
          axisLabel: {
            show: false // 隐藏刻度值
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        yAxis: {
          type: 'category',
          data: ['Brazil', 'Indonesia', 'USA', 'India', 'China', 'World']
        },
        series: [
          {
            label: {
              show: true,
              position: 'right'
            },
            name: '2011',
            type: 'bar',
            data: [18203, 23489, 29034, 104970, 131744, 630230]
          }
        ]
      },
      tableData: [{}, {}, {}, {}, {}],
      tableData1: [{}, {}, {}, {}, {}]
    }
  },
  mounted() {
    this.optionBarTop.color = this.w_color
    this.optionBarBottom.color = this.w_color
    this.optionBarMiddel.color = this.w_color

    this.barChartTop = echarts.init(document.getElementById('barChartTop'))
    this.barChartTop.setOption(this.optionBarTop, true)

    this.barChartBottom = echarts.init(document.getElementById('barChartBottom'))
    this.barChartBottom.setOption(this.optionBarBottom, true)

    this.barChartMiddel = echarts.init(document.getElementById('barChartMiddel'))
    this.barChartMiddel.setOption(this.optionBarMiddel, true)
  },
  methods: {
    name() {
    }
  }
}
</script>

<style lang="scss" scoped>
    h4{
        margin: 0 auto;
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
