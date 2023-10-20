<template>
  <div class="real_monitor">
    <!-- 机台产能报表 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-form inline>
          <el-form-item label="时间">
            <el-date-picker v-model="dateValue" size="small" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" value-format="yyyy-MM-dd HH:mm:ss" @change="changeDate" />
          </el-form-item>
          <el-form-item label="工艺段">
            <el-select v-model="getParams.process_name" clearable size="small" placeholder="请选择" @change="changeProcess" @visible-change="visibleChange1">
              <el-option v-for="item in lineList" :key="item.id" :label="item.process_name" :value="item.process_name" />
            </el-select>
          </el-form-item>
          <el-form-item label="站台">
            <el-select v-model="getParams.platform_name" clearable size="small" placeholder="请选择" @visible-change="visibleChange" @change="changeList">
              <el-option v-for="item in station_list" :key="item.platform_ID" :label="item.platform_name" :value="item.platform_name">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <!-- v-permission="['cache_device_conf','export']" -->
            <el-button type="blue" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-table id="out-table" :data="tableData" tooltip-effect="dark" style="width: 100%" stripe>
        <el-table-column label="站台名称" prop="platform_name" sortable />
        <el-table-column label="工艺段名称" prop="process_name" sortable />
        <el-table-column label="开始时间" prop="in_basket_num" sortable />
        <el-table-column label="结束时间" prop="out_basket_num" sortable />
      </el-table>
    </div>
  </div>
</template>

<script lang="js">
// import common from '@/utils/common'
import { setDate, exportExcel } from '@/utils/index'
import { platformInfo, currentSchedulerSearch, processSections, equipProductStatic } from '@/api/jqy'
export default {
  name: 'EquipStatic',
  components: {},
  data() {
    return {
      dateValue: [],
      tableData: [],
      btnExportLoad: false,
      getParams: {},
      loading: true,
      exportLoading: false,
      station_list: [],
      lineList: []
    }
  },
  created() {
    this.getTime()
  },
  mounted() {
  },
  methods: {
    async getTime(){
      try {
          const data = await currentSchedulerSearch('get', null, {})
          this.dateValue = [data.st,data.et]
          this.changeDate()
        } catch (e) {
        //
        }
    },
    changeDate(arr) {
      this.getParams.st = this.dateValue ? this.dateValue[0] : ''
      this.getParams.et = this.dateValue ? this.dateValue[1] : ''
      this.getList()
    },
    async getList() {
      try {
        this.loading = true
        const data = await equipProductStatic('get', null, { params: this.getParams })
        this.tableData = data.data || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getStationList() {
      try {
        let _id = this.lineList.find(d=>d.process_name===this.getParams.process_name).id
        this.getParams.platform_name = null
        const data = await platformInfo('get', null, { params: { all: 1,process:_id } })
        this.station_list = data || []
      } catch (e) {
      }
    },
    async getCurrentRouteList() {
      try {
        const data = await processSections('get', null, { params: { all: 1 } })
        this.lineList = data || []
      } catch (e) {
        //
      }
    },
    changeProcess(){
      this.getStationList()
      this.getList()
    },
    changeList() {
      this.getList()
    },
    exportFun() {
      this.exportLoading = true
      setTimeout(d => {
        exportExcel('机台产能报表')
        this.exportLoading = false
      }, 300)
    },
    visibleChange(bool) {
      if (bool) {
        // this.getStationList()
      }
    },
    visibleChange1(bool) {
      if (bool) {
        this.getCurrentRouteList()
      }
    },
  }
}
function getTime() {
  var date = new Date()
  var hour = date.getHours() // 时
  var minutes = date.getMinutes() // 分
  var seconds = date.getSeconds() // 秒
  // 给一位数的数据前面加 “0”
  if (hour >= 0 && hour <= 9) {
    hour = '0' + hour
  }
  if (minutes >= 0 && minutes <= 9) {
    minutes = '0' + minutes
  }
  if (seconds >= 0 && seconds <= 9) {
    seconds = '0' + seconds
  }
  return ' ' + hour + ':' + minutes + ':' + seconds
}
</script>

<style lang="scss" scoped>
  .el-tooltip__popper{
    max-width:50%
  }
</style>

