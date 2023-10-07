<template>
  <div class="real_monitor">
    <!-- 告警记录 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-form inline>
          <el-form-item label="最近发生时间">
            <el-date-picker v-model="getParams.dateValue" size="small" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" value-format="yyyy-MM-dd HH:mm:ss" @change="changeDate" />
          </el-form-item>
          <el-form-item label="告警描述">
            <el-input style="width:300px" v-model="getParams.alarm_desc" size="small" clearable placeholder="告警描述" />
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData" tooltip-effect="dark" style="width: 100%" stripe @sort-change="arraySpanMethod">
        <el-table-column label="告警场晨" prop="alarm_type" sortable="custom" :formatter="d=>{return d.alarm_type===1?'站台':'堆栈'}" />
        <el-table-column label="告警描述" prop="alarm_desc" sortable="custom" />
        <el-table-column label="严重性" prop="level" sortable="custom" />
        <el-table-column label="最近发生时间" prop="last_updated_time" sortable="custom" />
        <el-table-column label="重复次数" prop="alarm_times" sortable="custom" />
      </el-table>
      <el-footer id="footer">
        <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
      </el-footer>
    </div>
  </div>
</template>
  
<script lang="js">
import { monitorAlarm } from '@/api/base_w'
import page from '@/components/page'
import common from '@/utils/common'
  export default {
    name: 'AlarmLog',
    components: {page},
    data() {
      return {
        dateValue: [],
        tableData: [],
        btnExportLoad: false,
        getParams: {},
        loading: true,
        total: 0
      }
    },
    created() {
      this.getList()
    },
    mounted() {
    },
    methods: {
      changeDate(arr) {
        this.getParams.st = arr ? arr[0] : ''
        this.getParams.et = arr ? arr[1] : ''
        this.getParams.page = 1
        this.getList()
      },
      async getList() {
        try {
          this.loading = true
          const data = await monitorAlarm('get', null, { params: this.getParams })
          this.tableData = data.results || []
          this.total = data.count
          this.loading = false
        } catch (e) {
          this.loading = false
        }
    },
    async arraySpanMethod(val) {
      try {
        const obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams, obj)
        this.getList()
      } catch (e) {
        //
      }
    },
    changeList() {
        this.getParams.page = 1
        this.getList()
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    }
  }
</script>

<style lang="scss" scoped>
    .el-tooltip__popper{
      max-width:50%
    }
</style>
  
  