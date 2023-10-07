<template>
  <div class="real_monitor">
    <!-- 站台实时监控 -->
    <div v-loading="loading" class="center-box">
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
      <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" style="width: 100%" stripe @sort-change="arraySpanMethod">
        <el-table-column label="设备ID" prop="platform_ID" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.platform_ID" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.platform_ID }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="数量" prop="basket_num" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.basket_num" type="number" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.basket_num }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="状态" prop="task_status" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.task_status" placeholder="" clearable @change="changeList" size="small">
                <el-option v-for="item in ['T','F']" :key="item" :label="item" :value="item" />
              </el-select>
            </template>
            <template slot-scope="scope">
              {{ scope.row.task_status }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="设备名称" prop="platform_name" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.platform_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.platform_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="动作" prop="action" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.action" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in [{value:1,label:'PUT'},{value:2,label:'GET'}]" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </template>
            <template slot-scope="scope">
              {{ scope.row.action }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="屏蔽" prop="is_used" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.is_used" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in [{value:0,label:'已屏蔽'},{value:1,label:'未屏蔽'}]" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </template>
            <template slot-scope="scope">
              {{ scope.row.is_used ? '未屏蔽' : '已屏蔽' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="服务状态" prop="server_status" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.server_status" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in [{value:1,label:'Connected'},{value:0,label:'Connecting'}]" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </template>
            <template slot-scope="scope">
              {{ scope.row.server_status === 1 ? 'Connected' : 'Connecting' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="花篮更新时间" prop="update_time" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.update_time" size="small" style="width:200px" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
            </template>
            <template slot-scope="scope">
              <span :style="{'color':setColor(scope.row.update_time)?'red':''}">{{ scope.row.update_time?scope.row.update_time:'--' }}</span>
            </template>
          </el-table-column>
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
import common from '@/utils/common'
import { realTimeMonitor } from '@/api/jqy'
export default {
  name: 'RealMonitor',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      btnExportLoad: false,
      getParams: {},
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
        const data = await realTimeMonitor('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.all_data
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async arraySpanMethod(val) {
      try {
        let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams,obj)
        const data = await realTimeMonitor('get', null, { params: this.getParams})
        this.tableData = data.results || []
        this.total = data.all_data
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
    setColor(val){
      if(!val) return false
      var date = Date.parse(new Date(val));
      let dateC = Date.parse(new Date());
      let dateQ = date + 1800 * 1000
      if (dateQ < dateC) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

<style lang="scss">
  .el-tooltip__popper{
    max-width:50%
  }
</style>

