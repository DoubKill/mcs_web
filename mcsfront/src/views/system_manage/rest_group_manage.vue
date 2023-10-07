<template>
  <div>
    <!-- 休息位组管理 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <div class="botton-box">
        <el-button v-permission="['location_groups','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['location_groups','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
      </div>
      <el-table ref="multipleTable" :data="tableData" stripe @selection-change="handleSelectionChange" @sort-change="arraySpanMethod">
        <el-table-column type="selection" width="40" />
        <el-table-column label="休息位组编号" prop="group_code" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.group_code" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.group_code }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="休息位组名称" prop="group_name" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.group_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.group_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="已选择休息位" prop="group_name" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.location_names" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.location_names.join(',') }}
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
              <el-date-picker v-model="getParams.created_time" style="width:200px" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
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
              <el-date-picker v-model="getParams.last_updated_time" style="width:200px" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.last_updated_time?scope.row.last_updated_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template slot-scope="{row}">
            <el-button v-permission="['location_groups','change']" size="small" type="text" @click="editShow(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>
    <el-dialog :title="(currentObj.id?'编辑':'新建')+'休息位组'" :visible.sync="dialogVisible" width="1000px" :before-close="handleClose">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="休息位组编号" prop="group_code">
          <el-input v-model="currentObj.group_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="休息位组名称" prop="group_name">
          <el-input v-model="currentObj.group_name" size="small" />
        </el-form-item>
        <br>
        <el-form-item label="休息位">
          <el-table :data="tableData1" style="width:650px" tooltip-effect="dark" stripe>
            <el-table-column label="休息位">
              <template slot-scope="scope">
                <el-select v-model="scope.row.location" size="small" placeholder="请选择">
                  <el-option v-for="item in locationsList" :key="item.id" :label="item.location_name" :value="item.id">
                    <span style="float: left">{{ item.location_name }}</span>
                    <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
                  </el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="优先级">
              <template slot-scope="{row}">
                <el-input-number v-model="row.priority" controls-position="right" size="small" />
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button type="danger" icon="el-icon-delete" size="small" @click="dialogDeleteFun(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="text-align: center;">
            <el-button type="primary" size="small" @click="addDialogFun">插入一行</el-button>
          </div>
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
import { locations, locationGroups, locationGroupsDel } from '@/api/jqy'
import common from '@/utils/common'
import page from '@/components/page'
export default {
  name: 'RestGroupManage',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      tableData1: [],
      loading: false,
      locationsList: [],
      dialogVisible: false,
      currentVal: [],
      currentObj: {},
      rules: {
        group_code: [
          { required: true, message: '请填写休息位组编号', trigger: 'blur' }
        ],
        group_name: [
          { required: true, message: '请填写休息位组名称', trigger: 'blur' }
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
    async getOtherList() {
      try {
        const a = await Promise.all([
          locations('get', null, { params: { all: 1 }})
        ])
        this.locationsList = a[0] || []
      } catch (e) {
        //
      }
    },
    addDialogFun() {
      this.tableData1.push({})
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    async getList() {
      try {
        this.loading = true
        const data = await locationGroups('get', null, { params: this.getParams })
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
        const data = await locationGroups('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.tableData1 = []
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.getOtherList()
      this.dialogVisible = true
    },
    dialogDeleteFun(index) {
      this.tableData1.splice(index, 1)
    },
    editShow(row) {
      this.getOtherList()
      this.currentObj = Object.assign({}, row)
      this.tableData1 = row.locationgrouprelation_set || []
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
        locationGroupsDel('post', null, { data: { obj_ids: arr }})
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
      if (this.tableData1.length === 0) {
        this.$message.info('请选择休息位')
        return
      } else {
        this.currentObj.locationgrouprelation_set = this.tableData1
      }
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            console.log(isRepeat(this.tableData1))
            this.tableData1.forEach(d => {
              if (!d.location || !d.priority) {
                throw new Error('每行数据必填')
              }
            })
            if (isRepeat(this.tableData1)) {
              throw new Error('所选休息位有重复')
            }
            const _api = this.currentObj.id ? 'put' : 'post'
            this.btnLoading = true
            await locationGroups(_api, this.currentObj.id || null, { data: this.currentObj })
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
            if (e.message) {
              this.$message.info(e.message)
            }
          }
        } else {
          return false
        }
      })
    }
  }
}
function isRepeat(arr) {
  const a = arr.length
  // reduce第一个参数是遍历需要执行的函数，第二个参数是item的初始值
  var obj = {}
  arr = arr.reduce(function(item, next) {
    obj[next.location] ? '' : obj[next.location] = true && item.push(next)
    return item
  }, [])
  if (a !== arr.length) {
    return true
  } else {
    return false
  }
}
</script>

<style lang="scss" scoped>

</style>
