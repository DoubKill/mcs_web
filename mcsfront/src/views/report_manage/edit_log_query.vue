<template>
  <div class="edit_log_query">
    <!-- 操作履历 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="开始时间">
          <el-time-picker
            v-model="getParams.operator_time_after"
            value-format="HH:mm:ss"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            placeholder="开始时间"
          />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-time-picker
            v-model="getParams.operator_time_before"
            value-format="HH:mm:ss"
            :picker-options="{
              selectableRange: '00:00:00 - 23:59:59'
            }"
            placeholder="结束时间"
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
          v-permission="['user_operation_log','export']"
          type="modify"
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
        <el-table-column label="操作人">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.operator_user" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.operator_user }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作时间">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-date-picker
                value-format="yyyy-MM-dd"
                v-model="getParams.operator_time"
                type="date"
                @change="changeList" size="small"
                placeholder="">
              </el-date-picker>
            </template>
            <template slot-scope="scope">
              {{ scope.row.create_time?scope.row.create_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作类型">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.operator_type" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.operator_type }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作原因">
          <el-table-column width="300px">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.operator_reason" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.operator_reason }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作描述">
          <el-table-column show-overflow-tooltip min-width="220">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.operation_desc" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              <div
                style="cursor: pointer;overflow: hidden;text-overflow: ellipsis;"
                @click="dbclickDesc(row.operation_desc)"
              >{{ row.operation_desc }}</div>
            </template>
          </el-table-column>
        </el-table-column>
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
import { userOperationLog } from '@/api/jqy'
export default {
  name: 'EditLogQuery',
  components: { page },
  data() {
    return {
      dateValue: [],
      tableData: [],
      process_list: [],
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
    async getList() {
      try {
        this.loading = true
        const data = await userOperationLog('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    changeDate(arr) {
      this.getParams.operator_date_after = arr ? arr[0] : ''
      this.getParams.operator_date_before = arr ? arr[1] : ''
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = userOperationLog
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
    },
    dbclickDesc(val) {
      // 创建input标签
      var input = document.createElement('input')
      // 将input的值设置为需要复制的内容
      input.value = val
      // 添加input标签
      document.body.appendChild(input)
      // 选中input标签
      input.select()
      // 执行复制
      document.execCommand('copy')
      // 成功提示信息
      this.$message.success('复制成功!')
      // 移除input标签
      document.body.removeChild(input)
    }
  }
}
</script>

<style lang="scss">
  .el-tooltip__popper{
    max-width:50%
  }
</style>

