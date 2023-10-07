<template>
  <div>
    <!-- 检测点配置 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <div class="botton-box">
        <el-button v-permission="['env_location','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['env_location','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
      </div>
      <el-table ref="multipleTable" :data="tableData" stripe style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="40" />
        <el-table-column label="检测点名称" prop="location_name">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.location_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.location_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="所属工作区" prop="area_name">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.working_area" size="small" placeholder="" clearable @change="changeList" @visible-change="getOtherList">
                <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.working_area_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建人" prop="description">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.created_username" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.created_username }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建时间" prop="description">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.created_time" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.created_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="修改人" prop="last_update_username">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.last_update_username" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.last_update_username }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="修改时间" prop="last_updated_time">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.last_updated_time" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList"/>
            </template>
            <template slot-scope="{row}">
              {{ row.last_updated_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template slot-scope="{row}">
            <el-button v-permission="['env_location','change']" size="small" type="text" @click="editShow(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-footer id="footer">
        <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
      </el-footer>
    </div>
    <el-dialog :title="(currentObj.id?'编辑':'新建')+'检测点'" :visible.sync="dialogVisible" width="500px" :before-close="handleClose">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="检测点名称" prop="location_name">
          <el-input :disabled="!!currentObj.id" v-model="currentObj.location_name" size="small" @change="changeId" />
        </el-form-item>
        <el-form-item label="所属工作区" prop="working_area">
          <el-select :disabled="!!currentObj.id" v-model="currentObj.working_area" size="small" placeholder="请选择">
            <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
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
import { envCheckLocations, envCheckLocationsDel, workAreas } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'DetectionPoint',
  components: { page },
  data() {
    return {
      tableData: [],
      loading: false,
      dialogVisible: false,
      currentVal: [],
      currentObj: {},
      area_list: [],
      rules: {
        location_name: [
          { required: true, message: '请填写检测点名称', trigger: 'blur' }
        ],
        working_area: [
          { required: true, message: '请选择所属工作区', trigger: 'change' }
        ]
      },
      btnLoading: false,
      getParams: {},
      total: 0
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await envCheckLocations('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
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
    async getOtherList(val) {
      if (val) {
        try {
          const a = await workAreas('get', null, { params: { all: 1 } })
          this.area_list = a || []
        } catch (e) {
          //
        }
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.getOtherList(true)
      this.dialogVisible = true
    },
    editShow(row) {
      this.getOtherList(true)
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
        envCheckLocationsDel('post', null, { data: { obj_ids: arr } })
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
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            const _api = this.currentObj.id ? 'put' : 'post'
            this.btnLoading = true
            await envCheckLocations(_api, this.currentObj.id || null, { data: this.currentObj })
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
  