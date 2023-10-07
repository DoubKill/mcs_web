<template>
  <div>
    <!-- 花篮类别管理  未使用-->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="花篮类别">
          <el-input v-model="getParams.district_code" size="small" clearable placeholder="请输入花篮类别" />
        </el-form-item>
        <el-form-item label="花篮类别名称">
          <el-input v-model="getParams.district_name" size="small" clearable placeholder="请输入花篮类别名称" />
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
          label="花篮类别"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.district_code }}</template>
        </el-table-column>
        <el-table-column
          prop="district_name"
          label="花篮类别名称"
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
        <el-form-item label="花篮类别" prop="district_code">
          <el-input v-model="currentObj.district_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="花篮类别名称" prop="district_name">
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
import { districtInfos, districtInfosDel } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'FlowerType',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        district_code: [
          { required: true, message: '请填写花篮类别', trigger: 'blur' }
        ],
        district_name: [
          { required: true, message: '请填写花篮类别名称', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: false,
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
        const data = await districtInfos('get', null, { params: this.getParams })
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
        districtInfosDel('post', null, { data: { obj_ids: arr }})
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
            await districtInfos(_api, this.currentObj.id || null, { data: this.currentObj })
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
    }
  }
}
</script>

  <style lang="scss" scoped>

  </style>

