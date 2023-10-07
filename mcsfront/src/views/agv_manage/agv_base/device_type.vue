<template>
  <div>
    <!-- 设备类型 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="编号">
          <el-input v-model="getParams.type_code" size="small" clearable placeholder="编号" />
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="getParams.type_name" size="small" clearable placeholder="名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <el-button type="modify" icon="el-icon-download" size="small" :loading="btnExportLoad" @click="exportFun">导出</el-button>
        <el-button type="success" icon="el-icon-position" size="small">设置货架</el-button>
      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="40" />
        <el-table-column
          label="编号"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.type_code }}</template>
        </el-table-column>
        <el-table-column
          prop="type_name"
          label="名称"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="process_name"
          label="工序"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="destination"
          label="目标去向"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          label="循环编号"
          min-width="20"
          show-overflow-tooltip
        >
          <template slot-scope="scope">{{ scope.row.cycle_no }}</template>
        </el-table-column>
        <el-table-column
          prop="input_type"
          label="进料类型"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="output_type"
          label="出料类型"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          label="传篮模式"
          min-width="20"
          show-overflow-tooltip
        >
          <template slot-scope="scope">{{ scope.row.basket_mode }}</template>
        </el-table-column>
        <el-table-column
          prop="ordering"
          label="排序"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="ply_nums"
          label="缓存层数"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="docking_time"
          label="对接时间s"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          label="搬离时间s"
          min-width="20"
          show-overflow-tooltip
        >
          <template slot-scope="scope">{{ scope.row.remove_time }}</template>
        </el-table-column>
        <el-table-column
          prop="allowed_time"
          label="允许时间s"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="pitch_time"
          label="节拍时间s"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button size="small" type="text" @click="editShow(row)">修改</el-button>
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
      width="580px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" :inline="true">
        <el-form-item label="编号" prop="type_code">
          <el-input v-model="currentObj.type_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="名称" prop="type_name">
          <el-input v-model="currentObj.type_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="工序" prop="process">
          <el-select
            v-model="currentObj.process"
            size="small"
            placeholder="请选择"
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="目标去向">
          <el-select
            v-model="currentObj.destination"
            size="small"
            placeholder="请选择"
            clearable
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in tableData"
              :key="item.id"
              :label="item.type_name"
              :value="item.type_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="循环编号" prop="cycle_no">
          <el-select
            v-model="currentObj.cycle_no"
            size="small"
            placeholder="请选择"
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in cycle_no_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="进料类型" prop="input_type">
          <el-select
            v-model="currentObj.input_type"
            size="small"
            placeholder="请选择"
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in input_type_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="出料类型" prop="output_type">
          <el-select
            v-model="currentObj.output_type"
            size="small"
            placeholder="请选择"
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in output_type_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="传篮模式">
          <el-select
            v-model="currentObj.basket_mode"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in basket_mode_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="排序" prop="ordering">
          <el-input-number v-model="currentObj.ordering" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="缓存层数">
          <el-input-number v-model="currentObj.ply_nums" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="对接时间(s)">
          <el-input-number v-model="currentObj.docking_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="搬离时间(s)">
          <el-input-number v-model="currentObj.remove_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="允许时间(s)">
          <el-input-number v-model="currentObj.allowed_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="节拍时间(s)">
          <el-input-number v-model="currentObj.pitch_time" size="small" controls-position="right" :min="0" />
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
import page from '@/components/page'
import { deviceTypes, deviceTypesDel, productionProcesses } from '@/api/base_w'
import { getGlobalCodes } from '@/api/basics'
export default {
  name: 'DeviceType',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        type_code: [
          { required: true, message: '请填写编号', trigger: 'blur' }
        ],
        process: [
          { required: true, message: '请选择工序', trigger: 'change' }
        ],
        ply_nums: [
          { required: true, message: '请填写缓存层数', trigger: 'blur' }
        ],
        type_name: [
          { required: true, message: '请填写名称', trigger: 'blur' }
        ],
        destination: [
          { required: true, message: '请填写目标去向', trigger: 'blur' }
        ],
        cycle_no: [
          { required: true, message: '请选择循环编号', trigger: 'change' }
        ],
        input_type: [
          { required: true, message: '请选择进料类型', trigger: 'change' }
        ],
        output_type: [
          { required: true, message: '请选择出料类型', trigger: 'change' }
        ],
        ordering: [
          { required: true, message: '请填写排序', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      cycle_no_list: [],
      input_type_list: [],
      output_type_list: [],
      btnExportLoad: false,
      basket_mode_list: [],
      process_list: []
    }
  },
  created() {
    this.getList()
    this.getCode()
    this.getProcessList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await deviceTypes('get', null, { params: this.getParams })
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
    async getCode() {
      try {
        const p = await Promise.all([getGlobalCodes({ all: 1, type_name: '循环编号' }), getGlobalCodes({ all: 1, type_name: '进料类型' }), getGlobalCodes({ all: 1, type_name: '出料类型' }),
          getGlobalCodes({ all: 1, type_name: '传篮模式' })])

        this.cycle_no_list = p[0] || []
        this.input_type_list = p[1] || []
        this.output_type_list = p[2] || []
        this.basket_mode_list = p[3] || []
      } catch (e) {
        //
      }
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    handleSelectionChange(val) {
      this.currentVal = val
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
      this.currentObj = {}
      this.dialogVisible = false
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
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
        deviceTypesDel('post', null, { data: { obj_ids: arr }})
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
            await deviceTypes(_api, this.currentObj.id || null, { data: this.currentObj })
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
      const _api = deviceTypes
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

