<template>
  <div>
    <!-- AGV类型管理 -->
    <!-- <div class="top-search-box">
      <el-form :inline="true"> -->
    <!-- <el-form-item label="AGV类型名称">
          <el-input v-model="getParams.rack_type_name" size="small" clearable placeholder="AGV类型名称" />
        </el-form-item> -->
    <!-- <el-form-item label="一体车">
          <el-select
            v-model="getParams.is_bfi"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'是'},{id:false,name:'否'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item> -->
    <!-- <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div> -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['agv_type','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['agv_type','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <!-- <el-button type="modify" icon="el-icon-download" size="small" @click="exportFun">导出</el-button>  -->
      </div>
      <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" stripe style="width: 60%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="40" />
        <el-table-column prop="type_ID" label="AGV类型ID" min-width="20" />
        <el-table-column prop="type_name" label="AGV类型名称" min-width="20" />
        <!-- <el-table-column
          prop="is_bfi"
          label="是否一体车"
          min-width="10"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_bfi?'':'info'">{{ scope.row.is_bfi?'是':'否' }}</el-tag>
          </template>
        </el-table-column> -->
        <!-- <el-table-column
          prop="created_username"
          label="创建人"
          min-width="20"
        />
        <el-table-column
          prop="created_time"
          label="创建时间"
          min-width="20"
        />
        <el-table-column
          prop="last_update_username"
          label="修改人"
          min-width="20"
        />
        <el-table-column
          prop="last_updated_time"
          label="修改时间"
          min-width="20"
        /> -->
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button v-permission="['agv_type','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>

    <el-dialog :title="currentObj.id?'编辑':'新建'" :visible.sync="dialogVisible" width="500px" :before-close="handleClose" class="dialog-style">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="AGV类型ID" prop="type_ID">
          <el-input v-model="currentObj.type_ID" size="small" />
          <!-- :disabled="currentObj.id?true:false" -->
        </el-form-item>
        <el-form-item label="AGV类型名称" prop="type_name">
          <el-input v-model="currentObj.type_name" size="small" />
        </el-form-item>
        <!-- <el-form-item label="是否一体车" prop="is_bfi">
          <el-radio v-model="currentObj.is_bfi" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_bfi" :label="false">否</el-radio>
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
import { agvType, agvTypeDel } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'RackType',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        type_name: [
          { required: true, message: '请填写AGV类型名称', trigger: 'blur' }
        ],
        type_ID: [
          { required: true, message: '请填写AGV类型ID', trigger: 'blur' }
        ],
        axis_num: [
          { required: true, message: '请输入轴数', trigger: 'change' }
        ],
        basket_num: [
          { required: true, message: '请输入每轴花篮数', trigger: 'change' }
        ],
        is_bfi: [
          { required: true, message: '必填项', trigger: 'change' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await agvType('get', null, { params: this.getParams })
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
      this.currentObj = { is_bfi: true }
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
        this.$store.dispatch('settings/operateTypeSetting', '删除')
        agvTypeDel('post', null, { data: { obj_ids: arr } })
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
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await agvType(_api, this.currentObj.id || null, { data: this.currentObj })
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
      const _api = agvType
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

