<template>
  <div>
    <!-- AGV异常日志查询 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="AGV编号">
          <el-input
            v-model="getParams.agv_no"
            size="small"
            clearable
            placeholder="请输入AGV编号"
          />
        </el-form-item>
        <el-form-item label="订单号">
          <el-input
            v-model="getParams.task_no"
            size="small"
            clearable
            placeholder="请输入订单号"
          />
        </el-form-item>
        <el-form-item label="位置点">
          <el-select
            v-model="getParams.location"
            filterable
            clearable
            size="small"
            placeholder="请选择位置点"
            @visible-change="getPlatformList"
          >
            <el-option
              v-for="item in platform_list"
              :key="item.id"
              :label="item.location_code"
              :value="item.location_code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="异常描述">
          <el-input
            v-model="getParams.error_info"
            size="small"
            clearable
            placeholder="请输入异常描述"
          />
        </el-form-item>
        <el-form-item label="创建日期">
          <el-date-picker
            v-model="dateValue"
            size="small"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            @change="changeDate"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="success"
            icon="el-icon-search"
            size="small"
            @click="changeList"
          >搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div
      v-loading="loading"
      class="center-box"
    >
      <!-- <div class="botton-box">
        <el-button
          type="blue"
          icon="el-icon-download"
          size="small"
          :loading="btnExportLoad"
          @click="exportFun"
        >导出</el-button>
      </div> -->
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <el-table-column
          prop="agv_no"
          label="AGV编号"
          min-width="20"
        />
        <el-table-column
          prop="task_no"
          label="订单号"
          min-width="20"
        />
        <el-table-column
          prop="location"
          label="位置点"
          min-width="20"
        />
        <el-table-column
          prop="error_info"
          label="异常描述"
          min-width="20"
        />
        <el-table-column
          prop="begin_time"
          label="开始时间"
          min-width="20"
        />
        <el-table-column
          prop="end_time"
          label="结束时间"
          min-width="20"
        />
      </el-table>
    </div>
    <el-footer id="footer">
      <page
        :old-page="false"
        :total="total"
        :current-page="getParams.page"
        @currentChange="currentChange"
      />
    </el-footer>
  </div>
</template>

<script lang="js">
import page from '@/components/page'
import { agvErrorLog, cacheLocations } from '@/api/jqy'
export default {
  name: 'AgvLogQuery',
  components: { page },
  data() {
    return {
      dateValue: [],
      tableData: [],
      platform_list: [],
      total: 0,
      btnExportLoad: false,
      getParams: {},
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
  },
  mounted() {
  },
  methods: {
    async getPlatformList(val) {
      if (val) {
        try {
          const data = await cacheLocations('get', null, { params: { all: 1 }})
          this.platform_list = data || []
        } catch (e) {
        //
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await agvErrorLog('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    changeDate(arr) {
      this.getParams.st = arr ? arr[0] : ''
      this.getParams.et = arr ? arr[1] : ''
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = agvErrorLog
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    }
  }
}
</script>

<style lang="scss" scoped>

</style>

