<template>
  <div>
    <!-- 任务监控 -->
    <div
      class="top-search-box"
      style="padding:3px 16px"
    >
      <el-form :inline="true">
        <el-form-item label="任务号">
          <el-input
            v-model="getParams.task_no"
            size="small"
            clearable
            placeholder="任务号"
            @input="changeDebounce"
          />
        </el-form-item>
        <el-form-item label="任务类型">
          <el-select
            v-model="getParams.task_type"
            clearable
            size="small"
            placeholder="请选择任务类型"
            @change="changeList"
          >
            <el-option
              v-for="item in taskList"
              :key="item.type"
              :label="item.label"
              :value="item.type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="任务状态">
          <el-select
            v-model="getParams.state"
            clearable
            size="small"
            placeholder="请选择任务状态"
            @change="changeList"
          >
            <el-option
              v-for="item in itemsTask"
              :key="item.type"
              :label="item.label"
              :value="item.type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="站台">
          <el-select
            v-model="getParams.end_location"
            clearable
            size="small"
            placeholder="请选择站台"
            filterable
            @change="changeList"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in platform_list"
              :key="item.location_name"
              :label="item.platform_name"
              :value="item.location_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="小车号">
          <el-input
            v-model="getParams.agv_no"
            size="small"
            clearable
            placeholder="小车号"
            @input="changeDebounce"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="success"
            size="small"
            icon="el-icon-search"
            @click="changeList"
          >搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="center-box">
      <div class="botton-box">表头过滤：
        <el-select
          v-model="tabHearderMode"
          size="small"
          placeholder="表头过滤"
          style="width:60%"
          multiple
          @change="changeTabHearder"
        >
          <el-option
            v-for="item in tabHearder"
            :key="item.prop"
            :label="item.label"
            :value="item.prop"
          />
        </el-select>
      </div>
      <el-table
        ref="multipleTable"
        v-loading="loading"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
        @sort-change="arraySpanMethod"
      >
        <el-table-column v-for="(item) in newTabHearder" :prop="item.prop" :label="item.label" :min-width="item.width" :sortable="item.label==='任务创建时间'?'custom':false">
        </el-table-column>
      <el-table-column
        label="操作"
        width="70"
      >
        <template slot-scope="{row}">
          <el-button
            v-permission="['tasks','change']"
            size="small"
            type="text"
            @click="editState(1,row)"
          >取消</el-button>
          <!-- <el-button
            v-permission="['task_monitor','add']"
            size="small"
            type="text"
            @click="editState(2,row)"
          >强制完成</el-button> -->
        </template>
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
import { debounce } from '@/utils'
import page from '@/components/page'
import { taskMonitor, equipLocations } from '@/api/jqy'
export default {
  name: 'TaskMonitor',
  components: { page },
  data() {
    return {
      getParams: { },
      total: 0,
      tableData: [],
      platform_list: [],
      taskList: [
        // { type: 1, label: '导航' },
        { type: 2, label: '取货' },
        { type: 3, label: '卸货' },
        { type: 4, label: '取卸货' }
      ],
      itemsTask: [
        { type: 1, label:'已创建' },
        { type: 2, label:'待下发' },
        { type: 3, label:'已下发' },
        { type: 4, label:'已派车' },
        { type: 5, label:'已到达' },
        { type: 6, label:'开始对接' }
      ],
      tabHearderMode:['task_no','platform_name','axis1_action_name','axis3_action_name','axis1_package_name','axis3_package_name','priority','state_name','agv_no','created_time'],
      newTabHearder:[],
      tabHearder: [
        {label:'任务号',prop:'task_no',width:20},{label:'站台',prop:'platform_name',width:20},{label:'动作1',prop:'axis1_action_name',width:15},{label:'动作2',prop:'axis2_action_name',width:15},{label:'动作3',prop:'axis3_action_name',width:15},{label:'动作4',prop:'axis4_action_name',width:20},{label:'包号1',prop:'axis1_package_name',width:20},{label:'包号2',prop:'axis2_package_name',width:20},{label:'包号3',prop:'axis3_package_name',width:25},{label:'包号4',prop:'axis4_package_name',width:20},{label:'优先级',prop:'priority',width:10},{label:'任务状态',prop:'state_name',width:15},{label:'AGV车号',prop:'agv_no',width:20},{label:'任务创建时间',prop:'created_time',width:20}
      ]
    }
  },
  created() {
    this.getList()
  },
  methods: {
    changeDebounce() {
      debounce(this, 'changeList')
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
    async getList() {
      try {
        this.loading = true
        const data = await taskMonitor('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false

        this.changeTabHearder(this.tabHearderMode)
      } catch (e) {
        this.loading = false
      }
    },
    async visibleChange(val) {
      if (val) {
        try {
          const data = await equipLocations('get', null, { params: { all: 1 }})
          this.platform_list = data || []
        } catch (e) {
        //
        }
      }
    },
    async arraySpanMethod(val){
      try {
        let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + val.prop }
        Object.assign(this.getParams,obj)
        this.getList()
      } catch (e) {
        //
      }
    },
    editState(val, row) {
      this.$confirm('此操作将' + (val === 2 ? '强制完成' : '取消') + '此任务是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        taskMonitor('patch', row.id, { data: { 'task_state': val }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.changeList()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    changeTabHearder(VAL){
      this.newTabHearder = []
      this.tabHearder.forEach(dd=>{
        if(VAL.findIndex(d=>d === dd.prop)>-1){
          this.newTabHearder.push(dd)
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
    .w-tabs-style{
        margin-left:15px;
    }
    .pointer{
        margin-left: 10px;
        cursor: pointer;
    }
</style>
