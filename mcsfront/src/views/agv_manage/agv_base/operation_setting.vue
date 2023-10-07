<template>
  <div>
    <!-- 工序设置 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="工序编号">
          <el-input v-model="getParams.process_code" size="small" clearable placeholder="工序编号" />
        </el-form-item>
        <el-form-item label="工序名称">
          <el-input v-model="getParams.process_name" size="small" clearable placeholder="工序名称" />
        </el-form-item>
        <el-form-item label="启用标志">
          <el-select
            v-model="getParams.is_used"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'启用'},{id:false,name:'禁用'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['production_processes','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['production_processes','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['production_processes','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['production_processes','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <!-- <el-button type="modify" icon="el-icon-download" size="small" @click="exportFun">导出</el-button> -->
      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="40"
        />
        <el-table-column
          label="工序编号"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.process_code }}</template>
        </el-table-column>
        <el-table-column
          prop="process_name"
          label="工序名称"
          min-width="20"
        />
        <el-table-column
          prop="desc"
          label="工序描述"
          min-width="20"
        />
        <el-table-column
          prop="ordering"
          label="执行顺序"
          min-width="20"
        />
        <!-- <el-table-column
          prop="q_time"
          label="QTime(分钟)"
          min-width="20"
        />
        <el-table-column
          prop="task_threshold_time"
          label="任务阈值(分钟)"
          min-width="20"
        />
        <el-table-column
          label="是否强制先出先用"
          min-width="20"
        >
          <template slot-scope="scope">
            {{ scope.row.is_forced_fifo?'是':'否' }}
          </template>
        </el-table-column> -->
        <el-table-column
          label="启用标志"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_time"
          label="创建时间"
          min-width="20"
        />
        <el-table-column
          prop="last_updated_time"
          label="更新时间"
          min-width="20"
        />
        <el-table-column label="操作" width="140">
          <template slot-scope="scope">
            <el-button v-permission="['production_processes','change']" size="small" type="text" @click="editShow(scope.row)">修改</el-button>
            <el-button v-permission="['production_processes','change']" size="small" type="text" @click="moveUp(scope.$index,scope.row)">上移</el-button>
            <el-button v-permission="['production_processes','change']" size="small" type="text" @click="moveDown(scope.$index,scope.row,tableData)">下移</el-button>
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

    <el-dialog
      :title="currentObj.id?'编辑':'新建'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="工序编号" prop="process_code">
          <el-input v-model="currentObj.process_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="工序名称" prop="process_name">
          <el-input v-model="currentObj.process_name" size="small" />
        </el-form-item>
        <el-form-item label="工序描述" prop="desc">
          <el-input v-model="currentObj.desc" size="small" />
        </el-form-item>
        <el-form-item label="执行顺序" prop="ordering">
          <el-input-number v-model="currentObj.ordering" size="small" :disabled="currentObj.id?true:false" controls-position="right" :min="0" />
        </el-form-item>
        <!-- <el-form-item label="物料超时(分)">
          <el-input v-model="currentObj.timeout_period" size="small" />
        </el-form-item>
        <el-form-item label="最大在制(车)">
          <el-input v-model="currentObj.max_trains" size="small" />
        </el-form-item>
        <el-form-item label="换算率(车=>片)">
          <el-input v-model="currentObj.conversion" size="small" />
        </el-form-item> -->
        <!-- <el-form-item label="工序所处循环" prop="cycle_location">
          <el-select
            v-model="currentObj.cycle_location"
            clearable
            size="small"
            placeholder="请选择工序所处循环"
          >
            <el-option
              v-for="item in cycle_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="QTime(分钟)" prop="q_time">
          <el-input-number v-model="currentObj.q_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="任务阈值(分钟)" prop="task_threshold_time">
          <el-input-number v-model="currentObj.task_threshold_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="是否强制先出先用" prop="is_forced_fifo">
          <el-radio v-model="currentObj.is_forced_fifo" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_forced_fifo" :label="false">否</el-radio>
        </el-form-item> -->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { productionProcesses, productionProcessesDel } from '@/api/base_w'
import { getGlobalCodes } from '@/api/basics'
import { productionProcessesUpdate, processesChangeSequence } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'OperationSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      cycle_list: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        process_code: [
          { required: true, message: '请填写工序编号', trigger: 'blur' }
        ],
        process_name: [
          { required: true, message: '请填写工序名称', trigger: 'blur' }
        ],
        ordering: [
          { required: true, message: '请填写执行顺序', trigger: 'blur' }
        ],
        cycle_location: [
          { required: true, message: '请选择工序所处循环', trigger: 'blur' }
        ],
        q_time: [
          { required: true, message: '请填写QTime', trigger: 'blur' }
        ],
        task_threshold_time: [
          { required: true, message: '请填写任务阈值', trigger: 'blur' }
        ],
        is_forced_fifo: [
          { required: true, message: '请选择', trigger: 'change' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    this.getCycle()
  },
  methods: {
    async moveUp(index, row) {
      // if (index === 0) {
      //   this.$message({
      //     message: '处于顶端，不能继续上移',
      //     type: 'warning'
      //   })
      // } else {
      this.$store.dispatch('settings/operateTypeSetting', '上移')
      await processesChangeSequence('post', null, { data: { obj_id: row.id, operation_type: 'UP' }})
      this.getList()
      // }
    },
    async moveDown(index, row, tableData) {
      // if (index + 1 === tableData.length) {
      //   this.$message({
      //     message: '处于末端，不能继续下移',
      //     type: 'warning'
      //   })
      // } else {
      this.$store.dispatch('settings/operateTypeSetting', '下移')
      await processesChangeSequence('post', null, { data: { obj_id: row.id, operation_type: 'DOWN' }})
      this.getList()
      // }
    },
    async getCycle() {
      try {
        const data = await getGlobalCodes({ all: 1, type_name: '工序所处循环' })
        this.cycle_list = data || []
      } catch (e) {
        //
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await productionProcesses('get', null, { params: this.getParams })
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
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
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
    useFun(val, bool) {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      this.currentVal.forEach(d => {
        if (val === '禁用' && d.is_used) {
          arr.push(d.id)
        } else if (val === '启用' && !d.is_used) {
          arr.push(d.id)
        }
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', val)
        productionProcessesUpdate('post', null, { data: { 'obj_ids': arr }})
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
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    deleteFun() {
      if (!this.currentVal) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      this.currentVal.forEach(d => {
        arr.push(d.id)
      })
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', '删除')
        productionProcessesDel('post', null, { data: { obj_ids: arr }})
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
    submitFun() {
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await productionProcesses(_api, this.currentObj.id || null, { data: this.currentObj })
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
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = productionProcesses
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

