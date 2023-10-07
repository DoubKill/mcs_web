<template>
  <div>
    <!-- 异常码管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="设备类型">
          <el-input v-model="getParams.device_type" size="small" clearable placeholder="设备类型" />
        </el-form-item>
        <el-form-item label="异常编码">
          <el-input v-model="getParams.error_code" size="small" clearable placeholder="异常编码" />
        </el-form-item>
        <el-form-item label="异常级别">
          <el-input v-model="getParams.error_level" size="small" clearable placeholder="异常级别" />
        </el-form-item>
        <el-form-item label="异常描述">
          <el-input v-model="getParams.desc" size="small" clearable placeholder="异常描述" />
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
        <el-button type="modify" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
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
          label="设备类型"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.device_type }}</template>
        </el-table-column>
        <el-table-column
          prop="error_code"
          label="异常编码"
          min-width="20"
        />
        <el-table-column
          prop="error_level"
          label="异常级别"
          min-width="20"
        />
        <el-table-column
          prop="desc"
          label="异常描述"
          min-width="20"
        />
        <el-table-column label="操作" width="80">
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
        <el-form-item label="设备类型" prop="device_type">
          <el-input v-model="currentObj.device_type" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="异常编码" prop="error_code">
          <el-input v-model="currentObj.error_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="异常级别" prop="error_level">
          <el-input-number v-model="currentObj.error_level" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="异常描述" prop="desc">
          <el-input
            v-model="currentObj.desc"
            size="small"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 4}"
          />
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
import { errorCodes, errorCodesDel } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'ExceptionCode',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        device_type: [
          { required: true, message: '请填写设备类型', trigger: 'blur' }
        ],
        error_code: [
          { required: true, message: '请填写异常编码', trigger: 'blur' }
        ],
        error_level: [
          { required: true, message: '请填写异常级别', trigger: 'blur' }
        ],
        desc: [
          { required: true, message: '请填写描述信息', trigger: 'blur' }
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
        const data = await errorCodes('get', null, { params: this.getParams })
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
        errorCodesDel('post', null, { data: { obj_ids: arr }})
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
            await errorCodes(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.handleClose(null)
            this.changeList()
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
      const _api = errorCodes
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

