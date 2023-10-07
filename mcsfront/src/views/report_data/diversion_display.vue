<template>
  <div class="real_monitor">
    <!-- 分流展示 -->
    <div v-loading="loading" class="center-box">
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
        <el-table-column label="本线设备" prop="group_name" sortable="custom">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.group_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.group_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="分流来源设备" prop="shunt_platform_group">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.shunt_platform_group_name" size="small" placeholder="" clearable @change="changeList" @visible-change="getOtherList" filterable>
                <el-option v-for="item in groupList" :key="item.id" :label="item.group_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              {{ scope.row.shunt_platform_group.join() }}
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
  import { thresholdDisplay,platformGroup } from '@/api/base_w'
  export default {
    name: 'DiversionDisplay',
    components: { page },
    data() {
      return {
        tableData: [],
        total: 0,
        btnExportLoad: false,
        getParams: {},
        loading: true,
        groupList:[]
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
            if (this.getParams.shunt_platform_group_name === '') {
                delete this.getParams.shunt_platform_group_name
            }
            this.loading = true
            const data = await thresholdDisplay('get', null, { params: this.getParams })
            this.tableData = data.results || []
            this.total = data.count
            this.loading = false
        } catch (e) {
          this.loading = false
        }
      },
      async arraySpanMethod(val) {
        try {
            let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
            Object.assign(this.getParams,obj)
            const data = await thresholdDisplay('get', null, { params: this.getParams})
            this.tableData = data.results || []
            this.total = data.all_data
        } catch (e) {
          //
        }
      },
      async getOtherList(val) {
      if (val) {
        try {
          const a = await platformGroup('get', null, { params: { all: 1,fl_flag:1}})
          this.groupList = a || []
        } catch (e) {
          //
        }
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
      }
    }
  }
  </script>
  
  <style lang="scss">
    .el-tooltip__popper{
      max-width:50%
    }
  </style>
  
  