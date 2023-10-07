<template>
  <div>
    <!-- 物料标识 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="编号">
          <el-input v-model="getParams.identify_code" size="small" clearable placeholder="编号" />
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="getParams.identify_name" size="small" clearable placeholder="名称" />
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
        <el-button type="modify" icon="el-icon-download" size="small" @click="exportFun">导出</el-button>
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
          prop="identify_code"
          label="编号"
          min-width="10"
        />
        <el-table-column
          prop="identify_name"
          label="名称"
          min-width="20"
        />
        <el-table-column
          prop="is_full_flag"
          label="是否满篮"
          min-width="10"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_full?'':'info'">{{ scope.row.is_full_flag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="process_name"
          label="所属工序"
          min-width="10"
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
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="编号" prop="identify_code">
          <el-input v-model="currentObj.identify_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="名称" prop="identify_name">
          <el-input v-model="currentObj.identify_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="是否满篮" prop="is_full">
          <el-radio v-model="currentObj.is_full" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_full" :label="false">否</el-radio>
        </el-form-item>
        <el-form-item label="所属工序" prop="process">
          <el-select
            v-model="currentObj.process"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
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
import { productionProcesses } from '@/api/base_w'
import { materialIdentifies, materialIdentifiesDel } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'MaterialIdentification',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        identify_code: [
          { required: true, message: '请填写编号', trigger: 'blur' }
        ],
        identify_name: [
          { required: true, message: '请填写名称', trigger: 'blur' }
        ],
        is_full: [
          { required: true, message: '必填项', trigger: 'change' }
        ],
        process: [
          { required: true, message: '请选择所属工序', trigger: 'change' }
        ]
      },
      process_list: [],
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    this.getProcessList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await materialIdentifies('get', null, { params: this.getParams })
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
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.dialogVisible = true
      this.currentObj = { is_full: true }
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
    deleteFun() {
      if (!this.currentVal.length) {
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
        materialIdentifiesDel('post', null, { data: { obj_ids: arr }})
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
            await materialIdentifies(_api, this.currentObj.id || null, { data: this.currentObj })
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
      const _api = materialIdentifies
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

