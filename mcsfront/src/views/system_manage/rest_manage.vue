<template>
  <div>
    <!-- 休息位管理 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <div class="botton-box">
        <el-button v-permission="['locations','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['locations','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['locations','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['locations','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <el-button v-permission="['locations','add']" type="danger" icon="el-icon-refresh" size="small" @click="synchronousFun">同步</el-button>
      </div>
      <el-table ref="multipleTable" :data="tableData" stripe @selection-change="handleSelectionChange" @sort-change="arraySpanMethod">
        <el-table-column type="selection" width="40" />
        <el-table-column label="休息位名称" prop="location_name" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.location_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.location_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建人" prop="created_username" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.created_username" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_username?scope.row.created_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_time" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.created_time" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_time?scope.row.created_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="修改人" prop="last_updated_username" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.last_updated_username" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.last_update_username?scope.row.last_update_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="修改时间" prop="last_updated_time" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.last_updated_time" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.last_updated_time?scope.row.last_updated_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="启用标志" prop="is_used" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.is_used" size="small" clearable placeholder="" @change="changeList">
                <el-option v-for="item in [{name:'是',id:1},{name:'否',id:0}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'是':'否' }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template slot-scope="{row}">
            <el-button v-permission="['locations','change']" size="small" type="text" @click="editShow(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>
    <el-dialog :title="(currentObj.id?'编辑':'新建')+'休息位'" :visible.sync="dialogVisible" width="500px" :before-close="handleClose">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="休息位名称" prop="location_name">
          <el-input v-model="currentObj.location_name" size="small" />
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
import { locations, locationsDel, locationsUpdate, locationsSyncLocation } from '@/api/jqy'
import common from '@/utils/common'
import page from '@/components/page'
export default {
  name: 'RestManage',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      loading: false,
      dialogVisible: false,
      currentVal: [],
      currentObj: {},
      rules: {
        location_name: [
          { required: true, message: '请填写休息位名称', trigger: 'blur' }
        ]
      },
      btnLoading: false,
      getParams: {}
    }
  },
  created() {
    this.getList()
  },
  methods: {
    changeList() {
      this.getParams.page = 1
      this.getList()
    },

    async getList() {
      try {
        this.loading = true
        const data = await locations('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    async arraySpanMethod(val) {
      try {
        const obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams, obj)
        const data = await locations('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
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
    handleSelectionChange(val) {
      this.currentVal = val || []
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
        locationsUpdate('post', null, { data: { 'obj_ids': arr } })
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
    addFun() {
      this.dialogVisible = true
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
    },
    async synchronousFun() {
      try {
        await locationsSyncLocation('post', null, { params: {} })
        this.$message.success('同步休息位成功！')
        // this.$store.dispatch('settings/operateTypeSetting', '同步休息位')
        this.changeList()
      } catch (e) {
        //
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
        locationsDel('post', null, { data: { obj_ids: arr } })
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
            await locations(_api, this.currentObj.id || null, { data: this.currentObj })
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
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
