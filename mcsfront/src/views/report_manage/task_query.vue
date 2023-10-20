<template>
  <div class="task-query">
    <!-- 历史任务查询 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="查询时间">
          <el-date-picker v-model="dateValue" size="small" type="datetimerange" :clearable="true" value-format="yyyy-MM-dd HH:mm:ss" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" @change="changeDate" />
        </el-form-item>
        <el-form-item label="任务编号">
          <el-input v-model="getParams.task_no" size="small" clearable placeholder="任务编号" @input="changeDebounce" />
        </el-form-item>
        <el-form-item label="动作类型">
          <el-select v-model="getParams.task_type" clearable size="small" placeholder="请选择动作类型" @change="changeList">
            <el-option v-for="item in taskList" :key="item.type" :label="item.label" :value="item.type" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务状态">
          <el-select v-model="getParams.state" clearable size="small" placeholder="请选择任务状态" @change="changeList">
            <el-option v-for="item in itemsTask" :key="item.type" :label="item.label" :value="item.type" />
          </el-select>
        </el-form-item>
        <el-form-item label="站台">
          <el-select v-model="getParams.end_location" clearable size="small" placeholder="请选择站台" filterable @change="changeList" @visible-change="getPlatform">
            <el-option v-for="item in platform_list" :key="item.location_name" :label="item.platform_name" :value="item.location_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="小车号">
          <el-input v-model="getParams.agv_no" size="small" clearable placeholder="小车号" @input="changeDebounce" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
          <el-button v-permission="['history_tasks','export']" type="blue" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <el-table ref="multipleTable" v-loading="loading" :data="tableData" tooltip-effect="dark" style="width: 100%" stripe @sort-change="arraySpanMethod">
        <el-table-column v-for="(item) in newTabHearder" :prop="item.prop" :label="item.label" :min-width="item.width" :sortable="['创建时间','到位时间','结束时间'].includes(item.label)?'custom':false">

        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>
  </div>
</template>

<script lang="js">
import page from '@/components/page'
import { debounce } from '@/utils'
import { orderHistory, equipLocations, currentSchedulerSearch } from '@/api/jqy'
export default {
  name: 'TaskQuery',
  components: { page },
  data() {
    return {
      dateValue: [],
      taskList: [
        // { type: 1, label: '导航' },
        { type: 2, label: '取货' },
        { type: 3, label: '卸货' },
        { type: 4, label: '取卸货' }
      ],
      itemsTask: [
        { type: 7, label: '完成' },
        { type: 8, label: '失败' },
        { type: 9, label: '已取消' }
      ],
      tableData: [],
      platform_list: [],
      total: 0,
      btnExportLoad: false,
      getParams: {},
      btnLoading: false,
      loading: true,
      loadingStock: true,
      newTabHearder: [
        {label:'任务编号',prop:'task_no',width:15},
        {label:'站台ID',prop:'platform_ID',width:10},
        {label:'站台名称',prop:'platform_name',width:10},
        {label:'站台坐标',prop:'end_location',width:10},
        {label:'小车编号',prop:'agv_no',width:6},
        {label:'任务状态',prop:'state_name',width:6},
        {label:'动作类型',prop:'task_type_name',width:6},
        {label:'物料来源',prop:'origin_platform_name',width:10},
        {label:'创建时间',prop:'created_time',width:12},
        {label:'到位时间',prop:'arrived_time',width:12},
        {label:'结束时间',prop:'end_time',width:12},
        {label:'任务总耗时(秒)',prop:'task_time_consume',width:10},
        {label:'小车行走耗时(秒)',prop:'task_move_consume',width:10},
        {label:'任务交互耗时(秒)',prop:'task_interact_consume',width:10},
      ],
      exportLoading:false
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
    changeDebounce() {
      debounce(this, 'changeList')
    },
    async getPlatform(val) {
      if (val) {
        try {
          const data = await equipLocations('get', null, { params: { all: 1, is_used: true }})
          this.platform_list = data || []
        } catch (e) {
        //
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await orderHistory('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async arraySpanMethod(val){
      try {
        let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + val.prop }
        Object.assign(this.getParams,obj)
        this.getList()
      } catch (e) {
        //
      }
    },
    exportFun() {
      if(!this.getParams.st||!this.getParams.et){
        this.$message('日期不能为空，不得超过31天')
        return
      }
      if (getDaysBetween(this.getParams.st, this.getParams.et) > 31) {
        this.$message('查询日期间隔不得超过31天')
        return
      }
      this.exportLoading = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = orderHistory
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
      this.getParams.st = this.dateValue ? this.dateValue[0] : ''
      this.getParams.et = this.dateValue ? this.dateValue[1] : ''
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
// .task-query{

//   .top-search-box .el-input__inner{
//     // width: 180px !important
//   }
// }

</style>

