<template>
  <div class="station_date_back">
    <!-- 配置检查 -->
    <div v-loading="loading" style="margin:15px">
      <!-- <div class="botton-box">
        <el-form inline>
         <el-form-item label="时间">
            <el-date-picker v-model="getParams.dateValue" size="small" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" value-format="yyyy-MM-dd HH:mm:ss" @change="changeDate" />
          </el-form-item> 
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="changeList">刷新</el-button>
          </el-form-item>
        </el-form>
      </div> -->
      <el-table :data="tableData" tooltip-effect="dark" style="width: 100%" stripe @sort-change="arraySpanMethod" height="85vh">
        <el-table-column label="配置异常信息">
          <template slot-scope="{row}">
            {{ row }}
          </template>
        </el-table-column>
      </el-table>
      <!-- <el-footer id="footer">
        <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
      </el-footer> -->
    </div>
  </div>
</template>
  
  <script>
import { checkConf } from '@/api/base_w'
import { platformInfo } from '@/api/jqy'
// import page from '@/components/page'
import common from '@/utils/common'
export default {
  name: 'ConfigurationCheck',
  components: {},
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
    this.getList()
  },
  mounted() {
  },
  methods: {
    changeDate(arr) {
      this.getParams.start_time = arr ? arr[0] : ''
      this.getParams.end_time = arr ? arr[1] : ''
      this.getParams.page = 1
      this.getList()
    },
    async getStationList() {
      try {
        const data = await platformInfo('get', null, { params: { all: 1, platform_types: '1,3' } })
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
        const data = await checkConf('get', null, { params: this.getParams })
        this.tableData = data || []
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
        