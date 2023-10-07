<template>
  <div>
    <!-- 公用代码管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="类型名称">
          <el-input v-model="type_name" size="small" clearable placeholder="类型名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="typeNameChanged">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-row>
      <el-col :span="12">
        <div class="center-box">
          <div class="botton-box">
            <el-button v-permission="['global_types','add']" type="blue" icon="el-icon-plus" size="small" @click="showCreateGlobalCodeTypeDialog">新增</el-button>
            <el-button v-permission="['global_types','delete']" type="danger" icon="el-icon-delete" size="small" @click="handleGlobalCodeTypeDelete(currentVal)">删除</el-button>
          </div>
          <el-table
            ref="multipleTable"
            :data="tableData"
            tooltip-effect="dark"
            style="width: 100%"
            stripe
            row-key="id"
            highlight-current-row
            @selection-change="handleSelectionChange"
            @current-change="handleGlobalCodeTypesCurrentRowChange"
          >
            <el-table-column type="selection" width="40" />
            <!-- :reserve-selection="true" -->
            <el-table-column
              prop="type_no"
              label="类型代码"
            />
            <el-table-column
              prop="type_name"
              label="类型名称"
            />
            <el-table-column label="操作" width="60">
              <template slot-scope="{row}">
                <el-button v-permission="['global_types','change']" size="small" type="text" @click="showEditGlobalCodeTypeDialog(row)">修改</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <page
          :old-page="false"
          :total="total"
          :current-page="getParams.page"
          @currentChange="currentChange"
        />
      </el-col>
      <el-col :span="12">
        <div class="center-box">
          <div class="botton-box">
            <el-button v-permission="['global_types','add']" type="blue" icon="el-icon-plus" size="small" :disabled="!globalCodeTypesCurrentRow" @click="showCreateGlobalCodeDialog">新增</el-button>
            <el-button v-permission="['global_types','delete']" :disabled="!globalCodeTypesCurrentRow" type="danger" icon="el-icon-delete" size="small" @click="handleGlobalCodesDelete(currentVal2)">删除</el-button>
          </div>
          <el-table
            ref="multipleTable2"
            :data="globalCodes"
            style="width: 100%"
            @selection-change="handleSelectionChange2"
          >
            <el-table-column type="selection" width="40" />
            <el-table-column
              prop="global_no"
              label="公用代码"
            />
            <el-table-column
              prop="global_name"
              label="公用代码名称"
            />
            <el-table-column
              prop="description"
              label="备注"
            />
            <el-table-column label="操作" width="60">
              <template slot-scope="{row}">
                <el-button v-permission="['global_types','change']" size="small" type="text" :disabled="!globalCodeTypesCurrentRow" @click="showEditGlobalCodeDialog(row)">修改</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
    <el-dialog
      title="添加公用代码类型"
      :visible.sync="dialogCreateGlobalCodeTypeVisible"
    >
      <el-form :model="globalCodeTypeForm" label-width="120px">
        <el-form-item
          :error="globalCodeTypeFormError.type_no"
          label="类型编号"
        >
          <el-input v-model="globalCodeTypeForm.type_no" disabled />
        </el-form-item>
        <el-form-item
          :error="globalCodeTypeFormError.type_name"
          label="类型名称"
        >
          <el-input v-model="globalCodeTypeForm.type_name" />
        </el-form-item>
        <el-form-item
          :error="globalCodeTypeFormError.description"
          label="说明"
        >
          <el-input v-model="globalCodeTypeForm.description" />
        </el-form-item>
      </el-form>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogCreateGlobalCodeTypeVisible = false">取 消</el-button>
        <el-button
          type="primary"
          @click="handleCreateGlobalCodeType()"
        >确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="修改公用代码类型"
      :visible.sync="dialogEditGlobalCodeTypeVisible"
    >
      <el-form :model="globalCodeTypeForm" label-width="120px">
        <el-form-item
          :error="globalCodeTypeFormError.type_no"
          label="类型编号"
        >
          <el-input
            v-model="globalCodeTypeForm.type_no"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item
          :error="globalCodeTypeFormError.type_name"
          label="类型名称"
        >
          <el-input v-model="globalCodeTypeForm.type_name" />
        </el-form-item>
        <el-form-item
          :error="globalCodeTypeFormError.description"
          label="说明"
        >
          <el-input v-model="globalCodeTypeForm.description" />
        </el-form-item>
      </el-form>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogEditGlobalCodeTypeVisible = false">取 消</el-button>
        <el-button
          type="primary"
          @click="handleEditGlobalCodeType"
        >确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="添加公用代码"
      :visible.sync="dialogCreateGlobalCodeVisible"
    >
      <el-form :model="globalCodeForm" label-width="120px">
        <el-form-item
          :error="globalCodeFormError.global_no"
          label="公用代码编号"
        >
          <el-input v-model="globalCodeForm.global_no" disabled />
        </el-form-item>
        <el-form-item
          :error="globalCodeFormError.global_name"
          label="公用代码名称"
        >
          <el-input v-model="globalCodeForm.global_name" />
        </el-form-item>
        <el-form-item
          :error="globalCodeFormError.description"
          label="说明"
        >
          <el-input v-model="globalCodeForm.description" />
        </el-form-item>
      </el-form>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogCreateGlobalCodeVisible = false">取 消</el-button>
        <el-button
          type="primary"
          @click="handleCreateGlobalCode"
        >确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="修改公用代码"
      :visible.sync="dialogEditGlobalCodeVisible"
    >
      <el-form :model="globalCodeForm" label-width="120px">
        <el-form-item
          :error="globalCodeFormError.global_no"
          label="公用代码编号"
        >
          <el-input
            v-model="globalCodeForm.global_no"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item
          :error="globalCodeFormError.global_name"
          label="公用代码名称"
        >
          <el-input v-model="globalCodeForm.global_name" />
        </el-form-item>
        <el-form-item
          :error="globalCodeFormError.description"
          label="说明"
        >
          <el-input v-model="globalCodeForm.description" />
        </el-form-item>
      </el-form>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="dialogEditGlobalCodeVisible = false">取 消</el-button>
        <el-button
          type="primary"
          @click="handleEditGlobalCode"
        >确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getGlobalTypes, postGlobalTypes, putGlobalTypes, getGlobalCodes, postGlobalCodes, putGlobalCodes, globalCodesUrlBatchDestroy, commonCode, globalTypesUrlBatchDestroy } from '@/api/basics'
import page from '@/components/page'
export default {
  name: 'CodeManage',
  components: { page },
  data: function() {
    return {
      formLabelWidth: 'auto',
      tableData: [],
      type_name: '',
      globalCodeTypesCurrentRow: null,
      dialogCreateGlobalCodeTypeVisible: false,
      dialogEditGlobalCodeTypeVisible: false,
      globalCodeTypeForm: {

        type_no: '',
        type_name: '',
        description: '',
        use_flag: true
      },
      globalCodeTypeFormError: {},

      globalCodes: [],
      dialogCreateGlobalCodeVisible: false,
      dialogEditGlobalCodeVisible: false,
      globalCodeForm: {

        global_no: '',
        global_name: '',
        description: '',
        use_flag: true, // 0用
        global_type: null
      },
      globalCodeFormError: {},
      getParams: {
        page: 1
      },
      currentPage: 1,
      total: 1,
      currentVal: [],
      currentVal2: []
    }
  },
  computed: {
  },
  created() {
    this.getGlobalTypesList()
  },
  methods: {
    handleSelectionChange(arr) {
      this.currentVal = arr || []
    },
    handleSelectionChange2(arr) {
      this.currentVal2 = arr || []
    },
    afterGetData: function() {
      this.globalCodeTypesCurrentRow = null
    },
    typeNameChanged: function() { // 类型名搜索
      this.getParams.page = 1
      this.getParams['type_name'] = this.type_name
      this.getGlobalTypesList()
    },
    getGlobalTypesList() {
      getGlobalTypes(this.getParams).then(response => {
        this.tableData = response.results
        this.total = response.count
      })
    },
    clearGlobalCodeTypeForm: function() {
      this.globalCodeTypeForm = {
        type_no: '',
        type_name: '',
        description: '',
        use_flag: true
      }
    },
    clearGlobalCodeTypeFormError: function() {
      this.globalCodeTypeFormError = {
        type_no: '',
        type_name: '',
        description: '',
        use_flag: true
      }
    },
    showCreateGlobalCodeTypeDialog: function() {
      this.getCode(1)
      this.clearGlobalCodeTypeForm()
      this.clearGlobalCodeTypeFormError()
      this.dialogCreateGlobalCodeTypeVisible = true
    },
    async getCode(num) {
      try {
        const { results } = await commonCode({ code: num })
        if (num === 1) {
          this.globalCodeTypeForm.type_no = results
        } else {
          this.globalCodeForm.global_no = results
        }
      } catch (e) {
        //
      }
    },
    handleCreateGlobalCodeType: function() { // 创建全局代码类型
      this.clearGlobalCodeTypeFormError()
      const app = this
      this.$store.dispatch('settings/operateTypeSetting', '新增左侧')
      postGlobalTypes(this.globalCodeTypeForm)
        .then(function(response) {
          app.dialogCreateGlobalCodeTypeVisible = false
          app.$message.success(app.globalCodeTypeForm.type_name + '创建成功')
          app.currentChange(app.currentPage)
          app.$refs.multipleTable.setCurrentRow()
        }).catch(function(error) {
          for (var key in app.globalCodeTypeFormError) {
            if (error[key]) { app.globalCodeTypeFormError[key] = error[key].join(',') }
          }
        })
    },
    showEditGlobalCodeTypeDialog: function(row) {
      this.clearGlobalCodeTypeForm()
      this.clearGlobalCodeTypeFormError()
      this.globalCodeTypeForm = Object.assign({}, row)
      this.dialogEditGlobalCodeTypeVisible = true
    },
    handleEditGlobalCodeType: function() {
      const app = this
      this.$store.dispatch('settings/operateTypeSetting', '变更左侧')
      putGlobalTypes(this.globalCodeTypeForm, this.globalCodeTypeForm.id)
        .then(function(response) {
          app.dialogEditGlobalCodeTypeVisible = false
          app.$message.success(app.globalCodeTypeForm.type_name + '修改成功')
          app.currentChange(app.currentPage)
          app.$refs.multipleTable.setCurrentRow()
        }).catch(function(error) {
          for (var key in app.globalCodeTypeFormError) {
            if (error[key]) { app.globalCodeTypeFormError[key] = error[key].join(',') }
          }
        })
    },
    handleGlobalCodeTypeDelete: function(row) {
      var app = this
      if (!this.currentVal.length) {
        app.$message({
          message: '请选择列表数据'
        })
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
        this.$store.dispatch('settings/operateTypeSetting', '删除左侧')
        globalTypesUrlBatchDestroy('post', null, { data: { obj_ids: arr }})
          .then(function(response) {
            app.$message({
              type: 'success',
              message: '操作成功!'
            })
            if (app.tableData.length === 1 && app.currentPage > 1) {
              --app.currentPage
            }
            app.currentChange(app.currentPage)
            app.$refs.multipleTable.setCurrentRow()
          }).catch(function(error) {
            app.$message.error(error)
          })
      }).catch(function() {

      })
    },

    handleGlobalCodeTypesCurrentRowChange: function(row) {
      if (!row) { return }
      var app = this
      this.globalCodeTypesCurrentRow = row
      getGlobalCodes({ global_type_id: row.id })
        .then(function(response) {
          if (app.$refs.multipleTable2) {
            app.$refs.multipleTable2.clearSelection()
          }
          app.globalCodes = response
          // app.globalCodes.use_flag_b = app.globalCodes.use_flag ? 0 : 1
          app.globalCodeForm.global_type = row.id
        })
    },
    clearGlobalCodeForm: function() {
      this.globalCodeForm = {

        global_no: '',
        global_name: '',
        description: '',
        use_flag: true,
        global_type: this.globalCodeForm.global_type
      }
    },
    clearGlobalCodeFormError: function() {
      this.globalCodeFormError = {

        global_no: '',
        global_name: '',
        description: '',
        use_flag: ''
      }
    },
    showCreateGlobalCodeDialog: function() {
      if (!this.globalCodeForm.global_type) { return }
      this.clearGlobalCodeForm()
      this.clearGlobalCodeFormError()
      this.getCode(2)
      this.dialogCreateGlobalCodeVisible = true
    },
    handleCreateGlobalCode: function() {
      this.clearGlobalCodeFormError()
      // this.globalCodeForm.use_flag = this.globalCodeForm.use_flag_b ? 0 : 1
      var app = this
      this.$store.dispatch('settings/operateTypeSetting', '新增右侧')
      postGlobalCodes(this.globalCodeForm)
        .then(function(response) {
          app.dialogCreateGlobalCodeVisible = false
          app.$message.success(app.globalCodeForm.global_name + '创建成功')
          app.handleGlobalCodeTypesCurrentRowChange(app.globalCodeTypesCurrentRow)
        }).catch(function(error) {
          for (var key in app.globalCodeFormError) {
            if (error[key]) { app.globalCodeFormError[key] = error[key].join(',') }
          }
        })
    },
    showEditGlobalCodeDialog: function(row) {
      this.clearGlobalCodeForm()
      this.clearGlobalCodeFormError()
      this.globalCodeForm.id = row.id
      this.globalCodeForm.global_no = row.global_no
      this.globalCodeForm.global_name = row.global_name
      this.globalCodeForm.description = row.description
      this.globalCodeForm.use_flag = row.use_flag
      this.dialogEditGlobalCodeVisible = true
    },
    handleEditGlobalCode: function() {
      // this.globalCodeForm.use_flag = this.globalCodeForm.use_flag_b ? 0 : 1
      const app = this
      this.$store.dispatch('settings/operateTypeSetting', '变更右侧')
      putGlobalCodes(this.globalCodeForm, this.globalCodeForm.id)
        .then(function(response) {
          app.dialogEditGlobalCodeVisible = false
          app.$message.success(app.globalCodeForm.global_name + '修改成功')
          app.handleGlobalCodeTypesCurrentRowChange(app.globalCodeTypesCurrentRow)
        }).catch(function(error) {
          for (var key in app.globalCodeFormError) {
            // eslint-disable-next-line no-redeclare
            for (var key in app.globalCodeFormError) {
              if (error[key]) { app.globalCodeFormError[key] = error[key].join(',') }
            }
          }
        })
    },
    handleGlobalCodesDelete: function(row) {
      var app = this
      if (!this.currentVal2.length) {
        app.$message({
          message: '请选择列表数据'
        })
        return
      }
      const arr = []
      this.currentVal2.forEach(d => {
        arr.push(d.id)
      })
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', '删除右侧')
        globalCodesUrlBatchDestroy('post', null, { data: { obj_ids: arr }})
          .then(function(response) {
            app.$message({
              type: 'success',
              message: '操作成功!'
            })
            app.handleGlobalCodeTypesCurrentRowChange(app.globalCodeTypesCurrentRow)
          }).catch(function(error) {
            app.$message.error(error)
          })
      }).catch(function() {

      })
    },
    globalCodeTypeFormatter: function(row, column) {
      return this.boolFormatter(row.use_flag)
    },
    globalCodeUsedFlagFormatter: function(row, column) {
      return this.boolFormatter(row.use_flag)
    },
    boolFormatter: function(flag) {
      return flag ? 'Y' : 'N'
    },
    currentChange(page) {
      this.globalCodes = []
      this.currentPage = page
      this.getParams.page = page
      this.getGlobalTypesList()
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
