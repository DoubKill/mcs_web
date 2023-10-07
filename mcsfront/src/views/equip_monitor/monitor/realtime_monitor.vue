<template>
  <div>
    <!-- 实时运行 -->
    <div class="top-search-box">
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
              :key="item.platform_name"
              :label="item.platform_name"
              :value="item.location_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="小车号">
          <el-input
            v-model="getParams.rack_name"
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
            @click="changeList"
          >搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="center-box">
      <el-table
        ref="multipleTable"
        v-loading="loading"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <el-table-column
          prop="task_no"
          label="设备ID"
          min-width="25"
        />
        <el-table-column
          prop="end_location"
          label="数量"
          min-width="25"
        />
        <el-table-column
          prop="axis1_action_name"
          label="状态"
          min-width="20"
        />
        <el-table-column
          prop="axis2_action_name"
          label="动作2"
          min-width="20"
        />
        <el-table-column
          prop="axis3_action_name"
          label="设备名称"
          min-width="20"
        />
        <el-table-column
          prop="axis4_action_name"
          label="动作"
          min-width="20"
        />
        <el-table-column
          prop="axis1_package_name"
          label="屏蔽"
          min-width="20"
        />
        <el-table-column
          prop="axis2_package_name"
          label="服务状态"
          min-width="20"
        />
        <el-table-column
          prop="axis3_package_name"
          label="更新时间"
          min-width="20"
        />
        <el-table-column
          prop="axis4_package_name"
          label="子计数"
          min-width="20"
        />
      <!-- <el-table-column
        label="操作"
        width="120"
      >
        <template slot-scope="{row}">
          <el-button
            v-permission="['task_monitor','add']"
            size="small"
            type="text"
            @click="editState(1,row)"
          >取消</el-button>
          <el-button
            v-permission="['task_monitor','add']"
            size="small"
            type="text"
            @click="editState(2,row)"
          >强制完成</el-button>
        </template>
      </el-table-column> -->
      </el-table>
      <el-footer id="footer">
        <page
          :old-page="false"
          :total="total"
          :current-page="getParams.page"
          @currentChange="currentChange"
        />
      </el-footer>
    </div>
  </div>
</template>

<script lang="js">
import { debounce } from '@/utils/'
import page from '@/components/page'
import { taskMonitor, equipLocations } from '@/api/jqy'
export default {
  name: 'RealtimeMonitor',
  components: { page },
  data() {
    return {
      getParams: { },
      total: 0,
      tableData: [],
      platform_list: [],
      taskList: [
        { type: 1, label: '导航' },
        { type: 2, label: '取货' },
        { type: 3, label: '卸货' },
        { type: 4, label: '取卸货' }
      ],
      tabHearder: []
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
