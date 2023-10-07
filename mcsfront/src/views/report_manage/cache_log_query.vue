<template>
  <div>
    <!-- 缓存站异常日志查询 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="设备">
          <el-select
            v-model="getParams.equip_code"
            filterable
            clearable
            size="small"
            placeholder="请选择设备"
            @visible-change="getEquipList"
          >
            <el-option
              v-for="item in equip_list"
              :key="item.id"
              :label="item.equip_name"
              :value="item.equip_code"
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
          prop="equip_code"
          label="设备编号"
          min-width="20"
        />
        <el-table-column
          prop="equip_name"
          label="设备名称"
          min-width="20"
        />
        <el-table-column
          prop="error_info"
          label="异常描述"
          min-width="100"
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
import { basicsEquips } from '@/api/base_w'
import { cacheDeviceErrorLog } from '@/api/jqy'
export default {
  name: 'CacheLogQuery',
  components: { page },
  data() {
    return {
      dateValue: [],
      tableData: [],
      equip_list: [],
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
    async getEquipList(val) {
      if (val) {
        try {
          const data = await basicsEquips('get', null, { params: { all: 1, equip_type: 2 }})
          this.equip_list = data || []
        } catch (e) {
        //
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await cacheDeviceErrorLog('get', null, { params: this.getParams })
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
      const _api = cacheDeviceErrorLog
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
