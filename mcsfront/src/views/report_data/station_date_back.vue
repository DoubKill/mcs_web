<template>
  <div class="station_date_back">
    <!-- 站台任务追溯报表 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-form inline>
          <el-form-item label="时间">
            <el-date-picker v-model="dateValue" size="small" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" value-format="yyyy-MM-dd HH:mm:ss" @change="changeDate" />
          </el-form-item>
          <el-form-item label="目标站台">
            <el-select v-model="getParams.platform_ID" clearable size="small" placeholder="请选择" @visible-change="visibleChange" @change="changeList">
              <el-option v-for="item in station_list" :key="item.platform_ID" :label="item.platform_name" :value="item.platform_ID">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-table :data="tableData" tooltip-effect="dark" style="width: 100%" stripe @sort-change="arraySpanMethod">
        <el-table-column label="目标站台" prop="platform_name" />
        <el-table-column label="工艺段" prop="process_name" />
        <el-table-column label="AGV车号" prop="agv_no" />
        <el-table-column label="来源站台" prop="origin_platform_name" />
        <el-table-column label="接料时问" prop="receive_time" />
        <el-table-column label="送料时问" prop="end_time" />
      </el-table>
      <el-footer id="footer">
        <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
      </el-footer>
    </div>
  </div>
</template>
    
<script>
import { stationTaskTrack } from '@/api/base_w'
import { platformInfo, currentSchedulerSearch } from '@/api/jqy'
import page from '@/components/page'
import common from '@/utils/common'
export default {
  name: 'StationDateBack',
  components: { page },
  data() {
    return {
      dateValue: [],
      tableData: [],
      btnExportLoad: false,
      getParams: {},
      loading: true,
      total: 0,
      station_list: []
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
      this.getParams.page = 1
      this.getList()
    },
    async getStationList() {
      try {
        const data = await platformInfo('get', null, { params: { all: 1 } })
        this.station_list = data || []
      } catch (e) {
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getStationList()
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await stationTaskTrack('get', null, { params: this.getParams })
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
</style>
    
    