<template>
  <div class="report-forms">
    <!-- 检测报表 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="查询时间">
          <el-date-picker v-model="dateValue" size="small" type="datetimerange" :clearable="true" value-format="yyyy-MM-dd HH:mm:ss" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" @change="changeDate" />
        </el-form-item>
        <el-form-item label="检测状态">
          <el-select v-model="getParams.check_state" clearable size="small" placeholder="请选择检测状态" @change="changeList">
            <el-option v-for="item in statusList" :key="item.type" :label="item.label" :value="item.type" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否有效">
          <el-select v-model="getParams.is_useful" clearable size="small" placeholder="请选择检测状态" @change="changeList">
            <el-option v-for="item in [{label:'有效',type:true},{label:'失效',type:false}]" :key="item.type" :label="item.label" :value="item.type" />
          </el-select>
        </el-form-item>
        <el-form-item label="检测点名称">
          <el-select v-model="getParams.location_name" clearable size="small" placeholder="请选择检测点名称" @change="changeList" @visible-change="getEnvCheckList">
            <el-option v-for="item in envCheckList" :key="item.id" :label="item.location_name" :value="item.location_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="检测任务编号">
          <el-select v-model="getParams.task_no" clearable size="small" placeholder="请选择检测任务编号" @change="changeList" @visible-change="getTaskList">
            <el-option v-for="item in itemsTask" :key="item.id" :label="item.task_no" :value="item.task_no" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属工作区">
          <el-select v-model="getParams.working_area_name" size="small" placeholder="请选择所属工作区" clearable @change="changeList" @visible-change="getOtherList">
            <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.area_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="小车号">
          <el-input v-model="getParams.agv_no" size="small" clearable placeholder="小车号" @input="changeDebounce" />
        </el-form-item>

        <el-form-item style="float:right">
          <!-- <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button> -->
          <el-button v-permission="['env_check_history','export']" type="blue" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
        </el-form-item>
        <el-form-item style="float:right">
          <el-checkbox label="1" v-model="checked" @change="changeCheckbox">只显示最新检测结果</el-checkbox>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <el-table ref="multipleTable" v-loading="loading" :data="tableData" tooltip-effect="dark" style="width: 100%" :row-class-name="tableRowClassName">
        <el-table-column v-for="(item) in newTabHearder" :prop="item.prop" :label="item.label" :min-width="item.width">
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>
  </div>
</template>
  
<script>
import page from '@/components/page'
import { debounce } from '@/utils'
import { envCheckTasks, envCheckLocations, workAreas, envLocationCheckHistory } from '@/api/base_w'
export default {
  name: 'ReportForms',
  components: { page },
  data() {
    return {
      dateValue: [],
      statusList: [
        { type: 1, label: '正常' },
        { type: 2, label: '告警' },
        { type: 3, label: '报警' }
      ],
      itemsTask: [],
      envCheckList: [],
      tableData: [],
      total: 0,
      btnExportLoad: false,
      getParams: {},
      btnLoading: false,
      loading: true,
      loadingStock: true,
      newTabHearder: [
        { label: '检测点名称', prop: 'location_name', width: 15 },
        { label: '检测任务编号', prop: 'task_no', width: 10 },
        { label: '所属工作区', prop: 'working_area_name', width: 10 },
        { label: '小车号', prop: 'agv_no', width: 10 },
        { label: '创建时间', prop: 'created_time', width: 10 },
        { label: '上报时间', prop: 'report_time', width: 6 },
        { label: '温度', prop: 'indicator_value_1', width: 6 },
        { label: '湿度', prop: 'indicator_value_2', width: 6 },
        { label: '0.3微米离子数', prop: 'indicator_value_3', width: 10 },
        { label: '0.5微米离子数', prop: 'indicator_value_4', width: 12 },
        { label: '1微米离子数', prop: 'indicator_value_5', width: 12 },
        { label: '3微米离子数', prop: 'indicator_value_6', width: 12 },
        { label: '5微米离子数', prop: 'indicator_value_7', width: 10 }
      ],
      exportLoading: false,
      area_list: [],
      checked: null
    }
  },
  created() {
    this.getList()
  },
  mounted() {
  },
  methods: {
    changeDebounce() {
      debounce(this, 'changeList')
    },
    async getList() {
      try {
        this.loading = true
        const data = await envLocationCheckHistory('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getEnvCheckList(bool) {
      if (bool) {
        try {
          const data = await envCheckLocations('get', null, { params: { all: 1 } })
          this.envCheckList = data || []
        } catch (e) {
          //
        }
      }

    },
    async getTaskList(bool) {
      if (bool) {
        try {
          const data = await envCheckTasks('get', null, { params: { all: 1 } })
          this.itemsTask = data || []
        } catch (e) {
          //
        }
      }
    },
    async getOtherList(val) {
      if (val) {
        try {
          const a = await workAreas('get', null, { params: { all: 1 } })
          this.area_list = a || []
        } catch (e) {
          //
        }
      }
    },
    changeCheckbox(val) {
      this.getParams.new_flag = val ? 1 : null
      this.changeList()
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.check_state === 2) {
        return 'warning-row';
      } else if (row.check_state === 3) {
        return 'success-row';
      }
      return '';
    },
    exportFun() {
      if (!this.getParams.st || !this.getParams.et) {
        this.$message('日期不能为空，不得超过31天')
        return
      }
      if (getDaysBetween(this.getParams.st, this.getParams.et) > 31) {
        this.$message('查询日期间隔不得超过31天')
        return
      }
      this.exportLoading = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = envLocationCheckHistory
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.exportLoading = false
        }).catch(e => {
          this.exportLoading = false
        })
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    changeDate(arr) {
      this.getParams.st = arr ? arr[0] : ''
      this.getParams.et = arr ? arr[1] : ''
      this.changeList()
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    }
  }
}
function getDaysBetween(dateString1, dateString2) {
  var startDate = Date.parse(dateString1)
  var endDate = Date.parse(dateString2)
  if (startDate > endDate) {
    return 0
  }
  if (startDate === endDate) {
    return 1
  }
  var days = (endDate - startDate) / (1 * 24 * 60 * 60 * 1000)
  return days
}
  </script>
  
  <style lang="scss">
  .report-forms{
  .el-table .warning-row {
    background: oldlace;
  }
  .el-table .success-row {
    background: #f27070;
  }
  }
  
  </style>
  
  