<template>
  <div>
    <!-- AGV管理 未使用-->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="AGV编号">
          <el-input v-model="getParams.vehicle_code" size="small" clearable placeholder="请输入AGV编号" />
        </el-form-item>
        <el-form-item label="AGV名称">
          <el-input v-model="getParams.vehicle_name" size="small" clearable placeholder="请输入AGV名称" />
        </el-form-item>
        <el-form-item label="小车标记">
          <el-input v-model="getParams.vehicle_flag" size="small" clearable placeholder="请输入小车标记" />
        </el-form-item>
        <el-form-item label="启用标志">
          <el-select
            v-model="getParams.is_used"
            style="width:120px"
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
          <!-- <el-button type="success" size="small" @click="clearSearch">重置查询条件</el-button> -->
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['vehicle_infos','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['vehicle_infos','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['vehicle_infos','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['vehicle_infos','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          prop="vehicle_code"
          label="小车编号"
          min-width="20"
        />
        <el-table-column
          prop="vehicle_name"
          label="小车名称"
          min-width="20"
        />
        <!-- <el-table-column
          prop="district_code"
          label="区域"
          min-width="20"
        /> -->
        <el-table-column
          prop="dispatch_code"
          label="调度系统中的小车编号"
          min-width="20"
        />
        <el-table-column
          prop="vehicle_flag"
          label="小车标记"
          min-width="20"
        />
        <el-table-column
          label="启用标志"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button v-permission="['vehicle_infos','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
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
      :title="(currentObj.id?'编辑':'新建')+'小车信息'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="小车编号" prop="vehicle_code">
          <el-input v-model="currentObj.vehicle_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item><br>
        <el-form-item label="小车名称" prop="vehicle_name">
          <el-input v-model="currentObj.vehicle_name" size="small" />
        </el-form-item><br>
        <el-form-item label="小车标记" prop="vehicle_flag">
          <el-input v-model="currentObj.vehicle_flag" size="small" />
        </el-form-item><br>
        <el-form-item label="调度系统小车编号" prop="dispatch_code">
          <el-input v-model="currentObj.dispatch_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item><br>
        <!-- <el-form-item label="是否启用" prop="is_used">
          <el-radio v-model="currentObj.is_used" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_used" :label="false">否</el-radio>
        </el-form-item> -->
        <!-- <el-form-item label="区域" prop="district">
          <el-select
            v-model="currentObj.district"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in district_list"
              :key="item.district_code"
              :label="item.district_code"
              :value="item.id"
            />
          </el-select>
        </el-form-item> -->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="js">
// import { restArea, restAreaImportXlsx } from '@/api/base_w'
import { vehicleInfos, vehicleInfosUpdate, vehicleInfosDel } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'AgvManaging',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      district_list: [],
      dialogVisible: false,
      rules: {
        vehicle_code: [
          { required: true, message: '请填写小车编号', trigger: 'blur' }
        ],
        vehicle_name: [
          { required: true, message: '请填写小车名称', trigger: 'blur' }
        ],
        vehicle_flag: [
          { required: true, message: '请填写小车标记', trigger: 'blur' }
        ],
        dispatch_code: [
          { required: true, message: '请填写调度系统小车编号', trigger: 'blur' }
        ],
        district: [
          { required: true, message: '请选择区域', trigger: 'change' }
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
  mounted() {
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await vehicleInfos('get', null, { params: this.getParams })
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
    clearSearch() {
      this.getParams = { page: 1 }
      this.getList()
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
        vehicleInfosDel('post', null, { data: { obj_ids: arr }})
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
        vehicleInfosUpdate('post', null, { data: { 'obj_ids': arr }})
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
            await vehicleInfos(_api, this.currentObj.id || null, { data: this.currentObj })
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

