<template>
  <div>
    <!-- 花篮RFID追溯 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="花篮RFID">
          <el-input v-model="getParams.rfid" size="small" clearable placeholder="花篮RFID" />
        </el-form-item>
        <el-form-item label="传篮时间">
          <el-date-picker
            v-model="dateValue"
            size="small"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="yyyy-MM-dd HH:mm:ss"
            @change="changeDate"
          />
        </el-form-item>
        <el-form-item label="工序">
          <el-select
            v-model="getParams.process_id"
            clearable
            size="small"
            placeholder="请选择工序"
            style="width:160px"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="设备">
          <el-select
            v-model="getParams.equip_id"
            clearable
            size="small"
            placeholder="请选择设备"
            style="width:160px"
          >
            <el-option
              v-for="item in equip_list"
              :key="item.equip_name"
              :label="item.equip_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="站台">
          <el-select
            v-model="getParams.platform_id"
            clearable
            size="small"
            placeholder="请选择站台"
          >
            <el-option
              v-for="item in platform_list"
              :key="item.platform_name"
              :label="item.platform_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-getParams" size="small" @click="changeList">搜索</el-button>
          <el-button v-permission="['basket_transport','export']" type="blue" icon="el-icon-download" size="small" @click="exportFun">导出</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <el-table-column
          prop="rfid"
          label="花篮RFID"
          min-width="20"
        />
        <el-table-column
          prop="process_name"
          label="工序"
          min-width="20"
        />
        <el-table-column
          prop="equip_name"
          label="设备名称"
          min-width="20"
        />
        <el-table-column
          prop="platform_name"
          label="站台"
          min-width="20"
        />
        <el-table-column
          prop="axis"
          label="轴号"
          min-width="20"
        />
        <el-table-column
          prop="vehicle_code"
          label="AGV/货架编号"
          min-width="20"
        />
        <el-table-column
          prop="begin_time"
          label="传篮开始时间"
          min-width="20"
        />
        <el-table-column
          prop="end_time"
          label="传篮完成时间"
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

<script>
import { productionProcesses, basicsEquips } from '@/api/base_w'
import { basketTransport, platformInfo } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'BasketTracing',
  components: { page },
  data() {
    return {
      dateValue: [],
      tableData: [],
      equip_list: [],
      process_list: [],
      platform_list: [],
      total: 0,
      getParams: {},
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    this.getEquip()
    this.getProcessList()
  },
  methods: {
    changeDate(arr) {
      this.getParams.st = arr ? arr[0] : ''
      this.getParams.et = arr ? arr[1] : ''
    },
    async getEquip() {
      try {
        const data = await basicsEquips('get', null, { params: { all: 1, is_used: true }})
        const data1 = await platformInfo('get', null, { params: { all: 1, is_used: true }})
        this.equip_list = data.filter(d => d.is_used)
        this.platform_list = data1 || []
      } catch (e) {
        //
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await basketTransport('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getProcessList() {
      try {
        const data = await productionProcesses('get', null, { params: { all: 1, is_used: true }})
        this.process_list = data || []
      } catch (e) {
        //
      }
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = basketTransport
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    }
  }
}
</script>

  <style lang="scss" scoped>

  </style>

