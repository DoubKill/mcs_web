<template>
  <div>
    <!-- 缓存站任务管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="任务编号">
          <el-input v-model="getParams.task_no" size="small" clearable placeholder="任务编号" />
        </el-form-item>
        <!-- <el-form-item label="任务类型">
          <el-select
            v-model="getParams.task_type"
            clearable
            size="small"
          >
            <el-option
              v-for="item in []"
              :key="item.id"
              :label="item.line_code"
              :value="item.line_code"
            />
          </el-select>
        </el-form-item> -->
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="dateFinish"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd HH:mm:ss"
            :default-time="['00:00:00', '23:59:59']"
            @change="changeDate"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <!-- <div class="botton-box">
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
          <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
          <el-button type="modify" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
      </div> -->
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <!-- @selection-change="handleSelectionChange" -->
        <!-- <el-table-column
            type="selection"
            width="40"
          /> -->
        <el-table-column
          prop="task_no"
          label="任务编号"
        />
        <el-table-column
          prop="equip_code"
          label="设备编号"
        />
        <el-table-column
          prop="equip_name"
          label="设备名称"
        />
        <el-table-column
          prop="start_position"
          label="起始库位"
        />
        <el-table-column
          prop="end_position"
          label="截止库位"
        />
        <el-table-column
          prop="task_state"
          label="完成状态"
        />
        <el-table-column
          prop="created_time"
          label="创建时间"
        />
        <el-table-column
          prop="finish_time"
          label="完成时间"
        />
        <el-table-column
          prop="task_type"
          label="任务类型"
        />
        <!-- <el-table-column label="操作" width="80">
            <template slot-scope="{row}">
              <el-button size="small" type="text" @click="editShow(row)">修改</el-button>
            </template>
          </el-table-column> -->
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

    <el-dialog
      :title="currentObj.id?'编辑':'新建'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="区域编号" prop="district_code">
          <el-input v-model="currentObj.district_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="区域名称" prop="district_name">
          <el-input v-model="currentObj.district_name" size="small" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { cacheStationTasks } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'TaskBase',
  components: { page },
  data() {
    return {
      tableData: [],
      dateFinish: null,
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        district_code: [
          { required: true, message: '请填写区域编号', trigger: 'blur' }
        ],
        district_name: [
          { required: true, message: '请填写区域名称', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: false,
      exportLoading: false,
      resetLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await cacheStationTasks('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.dialogVisible = true
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
    },
    changeDate(date) {
      this.getParams.st = date ? date[0] : ''
      this.getParams.et = date ? date[1] : ''
      this.changeList()
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
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    submitFun() {
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            await cacheStationTasks(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.handleClose(null)
            this.getList()
            this.btnLoading = false
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    exportFun() {
      this.exportLoading = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = cacheStationTasks
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.exportLoading = false
        }).catch(e => {
          this.exportLoading = false
        })
    }
  }
}
</script>

  <style lang="scss" scoped>

  </style>

