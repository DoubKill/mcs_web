<template>
  <div>
    <!-- AGV状态监控列表 -->
    <!-- <el-tabs v-model="getParams.district_id" class="w-tabs-style" @tab-click="handleClick">
      <el-tab-pane v-for="item in process_list" :key="item.id" :label="item.district_name" :name="item.id" />
    </el-tabs> -->

    <div class="top-search-box" style="padding:3px 16px">
      <el-form :inline="true">
        <el-form-item label="任务号">
          <el-input v-model="getParams.task_no" size="small" clearable placeholder="任务号" />
        </el-form-item>
        <el-form-item label="任务类型">
          <el-select
            v-model="getParams.task_type"
            clearable
            size="small"
            placeholder="请选择任务类型"
          >
            <el-option
              v-for="item in [{name:'取货',id:1},{name:'卸货',id:2},{name:'取卸一体',id:3}]"
              :key="item.name"
              :label="item.name"
              :value="item.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="站台">
          <el-select
            v-model="getParams.platform_code"
            clearable
            size="small"
            placeholder="请选择站台"
            filterable
          >
            <el-option
              v-for="item in platform_list"
              :key="item.platform_name"
              :label="item.platform_name"
              :value="item.location__location_code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="小号车">
          <el-input v-model="getParams.vehicle_code" size="small" clearable placeholder="小号车" />
        </el-form-item>
        <!-- <el-form-item label="">
          <el-checkbox v-model="getParams.checked">异常库存</el-checkbox>
        </el-form-item> -->
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="getList">搜索</el-button>
        </el-form-item><br>
        <el-form-item label="小车状态">
          <div
            v-for="(item, index) in items"
            :key="item.label"
            style="display:inline-block;margin-left:15px"
          >
            <el-tag
              size="small"
              effect="dark"
              :style="{'background':colorVehicle[index]}"
              @click="clickVehicle(item)"
            >
              {{ state_cnt_dict[item.type]?state_cnt_dict[item.type]:0 }}
            </el-tag>
            <span
              class="pointer"
              :style="{'color':item.color?item.color:'#000'}"
              @click="clickTask(item.type)"
            >
              {{ item.label }}
            </span>
          </div>
          <span style="margin-left:20px;color:#b0a6a6">(点击状态进行过滤)</span>
          <span style="margin-left:20px">小车总数：{{ total_cnt }}</span>
        </el-form-item>
      </el-form>
      <el-table
        :data="tableData"
        style="width: 100%"
        border
        :span-method="objectSpanMethod"
      >
        <el-table-column
          prop="vehicle_code"
          label="小车号"
          width="80"
        />
        <el-table-column
          prop="state"
          label="小车状态"
          width="100"
        >
          <template slot-scope="{row}">
            <el-tag
              effect="dark"
              :style="{'background':colorVehicle[items.findIndex(d=>d.type === row.state)]}"
            >
              {{ row.state?items.find(d=>d.type === row.state).label:null }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="level"
          label="层"
        />
        <el-table-column
          prop="axis"
          label="轴号"
        />
        <el-table-column
          prop="basket_num"
          label="花篮实际数量"
        />
        <el-table-column
          prop="stock_num"
          label="库存数量"
        />
        <el-table-column
          prop="basket_time"
          label="花篮时间"
        />
        <el-table-column
          prop="task_no"
          label="任务号"
        />
        <el-table-column
          prop="platform_name"
          label="对接站台"
        />
        <el-table-column
          prop="task_type_name"
          label="任务类型"
        />
        <el-table-column
          prop="material_type_name"
          label="物料"
          min-width="160"
        />
      </el-table>
    </div>
  </div>
</template>

<script>
import { monitorAgvTask } from '@/api/base_w'
import { platformInfo } from '@/api/jqy'
export default {
  name: 'AgvMonitorList',
  data() {
    return {
      activeName: '0',
      getParams: { },
      // colorVehicle: ['#656f71', '#48b596', '#95c454', '#f1b253', '#3d40c3', '#e06377', '#4ea8dc', '#d33e47'],
      colorVehicle: ['#656f71', '#d33e47', '#48b596', '#95c454', '#4ea8dc'],
      // items: [
      //   { type: 0, label: '离线' },
      //   { type: 1, label: '空闲' },
      //   { type: 2, label: '任务' },
      //   { type: 3, label: '异常' },
      //   { type: 4, label: '挂起' },
      //   { type: 5, label: '暂停' },
      //   { type: 6, label: '登录中' }
      // ],
      items: [
        { type: 1, label: '已移除' },
        { type: 2, label: '故障' },
        { type: 3, label: '空闲' },
        { type: 4, label: '任务' },
        { type: 5, label: '充电中' }
      ],
      tableData: [],
      total_cnt: 0,
      state_cnt_dict: {},
      // process_list: [],
      statisticalQuantity: [],
      spanArr: [],
      platform_list: []
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/agv-monitor-list') {
          this.getOtherList()
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
    // this.getOtherList()
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  methods: {
    changeList() {
      delete this.getParams.filter_state
      this.items.forEach(d => { delete d.color })
      this.getList()
    },
    async getList() {
      try {
        this.loading = true
        const obj = Object.assign({}, this.getParams)
        // obj.district_id = obj.district_id === '0' ? '' : obj.district_id
        const data = await monitorAgvTask('get', null, { params: obj })
        this.tableData = data.data || []
        this.state_cnt_dict = data.state_cnt_dict
        this.total_cnt = data.total_cnt
        const arr = [0, 0, 0, 0, 0, 0, 0]
        this.tableData.forEach(dd => {
          if (dd.state === '离线') {
            arr[0] += 1
          } else if (dd.state === '空闲') {
            arr[1] += 1
          } else if (dd.state === '任务') {
            arr[2] += 1
          } else if (dd.state === '异常') {
            arr[3] += 1
          } else if (dd.state === '挂起') {
            arr[4] += 1
          } else if (dd.state === '暂停') {
            arr[5] += 1
          } else if (dd.state === '登录中') {
            arr[6] += 1
          }
        })
        this.statisticalQuantity = arr

        this.spanArr = []
        this.pos = null
        this.spanArr1 = []
        this.pos1 = null
        for (var i = 0; i < this.tableData.length; i++) {
          if (i === 0) {
            this.spanArr.push(1)
            this.pos = 0
            this.spanArr1.push(1)
            this.pos1 = 0
          } else {
            if (this.tableData[i].vehicle_code === this.tableData[i - 1].vehicle_code) {
              this.spanArr[this.pos] += 1
              this.spanArr.push(0)
            } else {
              this.spanArr.push(1)
              this.pos = i
            }
            if (this.tableData[i].vehicle_code === this.tableData[i - 1].vehicle_code && this.tableData[i].level === this.tableData[i - 1].level) {
              this.spanArr1[this.pos1] += 1
              this.spanArr1.push(0)
            } else {
              this.spanArr1.push(1)
              this.pos1 = i
            }
          }
        }
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getOtherList() {
      try {
        const a = await Promise.all([
          // districtInfos('get', null, { params: { all: 1, is_used: true }}),
          platformInfo('get', null, { params: { all: 1, is_used: true }})
        ])
        // this.process_list = a[0] || []
        // this.process_list.forEach(d => {
        //   d.id = (d.id).toString()
        // })
        // this.process_list.unshift({ district_name: '全部', id: '0' })
        this.platform_list = a[0] || []
        this.getList()
      } catch (e) {
        //
      }
    },
    clickTask(val) {
      this.getParams.filter_state = val
      this.items.forEach(d => {
        if (d.type === val) {
          if (d.color) {
            delete d.color
            delete this.getParams.filter_state
          } else {
            d.color = '#5A9CF8'
          }
        } else {
          delete d.color
        }
      })
      this.getList()
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if ([0, 1].includes(columnIndex) && this.spanArr) {
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
      if ([2].includes(columnIndex) && this.spanArr1) {
        const _row = this.spanArr1[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
    },
    handleClick() {
      this.getList()
    },
    clickVehicle(item) {
      // this.getParams.state = item.type
      // this.getList()
    }
  }
}
</script>

<style lang="scss" scoped>
    .pointer{
        cursor: pointer;
    }
    .w-tabs-style{
        margin-left:15px;
    }
</style>
