<template>
  <div class="real_monitor">
    <!-- AGV物料监控 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">表头过滤：
        <el-select v-model="tabHearderMode" size="small" placeholder="表头过滤" style="width:60%" multiple @change="changeTabHearder">
          <el-option v-for="item in tabHearder" :key="item.prop" :label="item.label" :value="item.prop" />
        </el-select>
      </div>
      <el-table :data="tableData" tooltip-effect="dark" style="width: 100%" stripe height="83vh">
        <template v-for="(item) in newTabHearder">
          <el-table-column v-if="item.label==='AGV车号'" label="AGV车号" prop="vehicle_code" sortable>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="getParams.vehicle_code" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.vehicle_code }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='轨道1-包号'" label="轨道1-包号" prop="ax1_material" sortable>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="getParams.ax1_material" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.ax1_material }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='轨道2-包号'" label="轨道2-包号" prop="ax2_material" sortable>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="getParams.ax2_material" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.ax2_material }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='轨道3-包号'" label="轨道3-包号" prop="ax3_material" sortable>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="getParams.ax3_material" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.ax3_material }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='轨道4-包号'" label="轨道4-包号" prop="ax4_material" sortable>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="getParams.ax4_material" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.ax4_material }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='来源站台'" label="来源站台" prop="platform_name" sortable>
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-input v-model="getParams.platform_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.platform_name }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='下料时间'" label="下料时间" prop="out_time" sortable="custom">
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-date-picker v-model="getParams.out_time" size="small" style="width:200px" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
              </template>
              <template slot-scope="scope">
                {{ scope.row.out_time?scope.row.out_time:'--' }}
              </template>
            </el-table-column>
          </el-table-column>
          <el-table-column v-if="item.label==='是否超期'" label="是否超期" prop="is_expired">
            <el-table-column>
              <template slot="header" slot-scope="scope">
                <el-select v-model="getParams.is_expired" size="small" clearable placeholder="" @change="changeList">
                  <el-option v-for="item in [{name:'是',id:1},{name:'否',id:0}]" :key="item.name" :label="item.name" :value="item.id" />
                </el-select>
              </template>
              <template slot-scope="scope">
                <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_expired?'danger':'info'">{{ scope.row.is_expired?'是':'否' }}</el-tag>
              </template>
            </el-table-column>
          </el-table-column>
        </template>
      </el-table>
    </div>
  </div>
</template>
  
  <script>
import common from '@/utils/common'
import { agvPackage } from '@/api/base_w'
export default {
  name: 'RealMonitor',
  data() {
    return {
      tableData: [],
      btnExportLoad: false,
      getParams: {},
      loading: true,
      tabHearderMode: ['vehicle_code', 'ax1_material', 'ax3_material', 'platform_name', 'out_time', 'is_expired'],
      tabHearder: [
        { label: 'AGV车号', prop: 'vehicle_code', width: 20 },
        { label: '轨道1-包号', prop: 'ax1_material', width: 20 },
        { label: '轨道2-包号', prop: 'ax2_material', width: 20 },
        { label: '轨道3-包号', prop: 'ax3_material', width: 20 },
        { label: '轨道4-包号', prop: 'ax4_material', width: 20 },
        { label: '来源站台', prop: 'platform_name', width: 20 },
        { label: '下料时间', prop: 'out_time', width: 20 },
        { label: '是否超期', prop: 'is_expired', width: 20 },
      ],
      newTabHearder: []
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/material-monitor') {
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
          }, 5000)
        } else {
          window.clearInterval(this._setInterval)
        }
      },
      deep: true, // 深度监听
      immediate: true // 第一次初始化渲染就可以监听到
    }
  },
  created() {
  },
  mounted() {
  },
  methods: {
    async getList() {
      try {
        this.loading = false
        const data = await agvPackage('get', null, { params: this.getParams })
        this.tableData = data.data || []
        this.loading = false
        this.changeTabHearder(this.tabHearderMode)
      } catch (e) {
        this.loading = false
      }
    },
    async arraySpanMethod(val) {
      try {
        let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams, obj)
        const data = await agvPackage('get', null, { params: this.getParams })
        this.tableData = data.data || []
      } catch (e) {
        //
      }
    },
    changeList() {
      this.getList()
    },
    changeTabHearder(VAL) {
      this.newTabHearder = []
      this.tabHearder.forEach(dd => {
        if (VAL.findIndex(d => d === dd.prop) > -1) {
          this.newTabHearder.push(dd)
        }
      })
    }
  }
}
  </script>
  
  <style lang="scss">
  .real_monitor{
    .el-tooltip__popper{
      max-width:50%
    }
  }
  </style>
  
  