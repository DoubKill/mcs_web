<template>
  <div>
    <!-- 工作区管理 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <div class="botton-box">
        <el-button v-permission="['work_area','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['work_area','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        stripe
        style="width: 60%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="40"
        />
        <el-table-column label="工作区ID" prop="area_ID">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.area_ID" prefix-icon="el-icon-search" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.area_ID }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="工作区名称" prop="area_name">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.area_name" prefix-icon="el-icon-search" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.area_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="AGV类型" prop="agv_type_name">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.agv_type_name" prefix-icon="el-icon-search" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.agv_type_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="描述" prop="description">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.description" prefix-icon="el-icon-search" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.description }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column label="RCS地址" prop="rcs_address">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.rcs_address" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.rcs_address }}
            </template>
          </el-table-column>
        </el-table-column> -->
        <el-table-column label="操作" width="80">
          <template slot-scope="{row}">
            <el-button v-permission="['work_area','change']" size="small" type="text" @click="editShow(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog
      :title="(currentObj.id?'编辑':'新建')+'工作区'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="工作区ID" prop="area_ID">
          <el-input v-model="currentObj.area_ID" size="small" @change="changeId" />
        </el-form-item>
        <el-form-item label="工作区名称" prop="area_name">
          <el-input v-model="currentObj.area_name" size="small" />
        </el-form-item>
        <el-form-item label="agv类型" prop="agv_type">
          <el-select v-model="currentObj.agv_type" size="small" placeholder="请选择">
            <el-option v-for="(item) in ageTypeList" :key="item.id" :label="item.type_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="currentObj.description" size="small" />
        </el-form-item>
        <!-- <el-form-item label="RCS地址" prop="rcs_address">
          <el-input v-model="currentObj.rcs_address" size="small" />
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
import { workAreas, workAreasDel } from '@/api/base_w'
import { agvType } from '@/api/jqy'
export default {
  name: 'WorkspaceManage',
  data() {
    return {
      tableData: [],
      loading: false,
      dialogVisible: false,
      currentVal: [],
      currentObj: {},
      rules: {
        area_ID: [
          { required: true, message: '请填写工作区ID', trigger: 'blur' }
        ],
        area_name: [
          { required: true, message: '请填写工作区名称', trigger: 'blur' }
        ],
        agv_type: [
          { required: true, message: '请选择agv类型', trigger: 'change' }
        ]
        // rcs_address: [
        //   { required: true, message: '请填写RCS地址', trigger: 'blur' }
        // ]
      },
      btnLoading: false,
      getParams: {},
      ageTypeList: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await workAreas('get', null, { params: this.getParams })
        this.tableData = data || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getAgv() {
      try {
        const data = await agvType('get', null, { params: {all:1} })
        this.ageTypeList = data
      } catch (e) {
        //
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = { }
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.getAgv()
      this.dialogVisible = true
    },
    editShow(row) {
      this.getAgv()
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
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
        workAreasDel('post', null, { data: { obj_ids: arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', '删除')
            this.getList()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    submitFun() {
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.area_ID.length > 2) {
              this.$message('工作区ID最多2个数字')
              return
            }
            if (this.currentObj.area_ID.length === 1) {
              this.currentObj.area_ID = '0' + this.currentObj.area_ID
            }
            this.btnLoading = true
            await workAreas(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.handleClose(null)
            this.getList()
            this.btnLoading = false
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    changeId(val) {

    }
  }
}
</script>

<style lang="scss" scoped>

</style>
