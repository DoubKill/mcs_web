<template>
  <div
    v-loading="loading"
    class="roles-manage"
  >
    <!-- 角色管理 -->
    <div class="center-box">
      <div class="botton-box">
        <el-button
          v-permission="['roles','add']"
          type="blue"
          icon="el-icon-plus"
          size="small"
          @click="showCreateGroupDialog"
        >新建</el-button>
        <!-- <el-button
          v-permission="['group_extension','update']"
          style="margin-left:8px"
          type="danger"
          icon="el-icon-turn-off"
          size="small"
          @click="useFun('禁用')"
        >禁用</el-button>
        <el-button
          v-permission="['group_extension','update']"
          type="danger"
          icon="el-icon-open"
          size="small"
          @click="useFun('启用')"
        >启用</el-button> -->
        <el-button
          v-permission="['roles','delete']"
          type="danger"
          icon="el-icon-delete"
          size="small"
          @click="deleteFun"
        >删除</el-button>
      </div>
      <el-table
        v-loading="loadingTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%;padding: 0 10px 0 10px;"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="40"
        />
        <el-table-column label="角色代码" prop="group_code">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.group_code" prefix-icon="el-icon-search" size="small" clearable @input="groupCodeChanged" />
            </template>
            <template slot-scope="{row}">
              {{ row.group_code }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="角色名称" prop="name">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.name" prefix-icon="el-icon-search" size="small" clearable @input="nameChanged" />
            </template>
            <template slot-scope="{row}">
              {{ row.name }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column
        prop="section_name"
        label="部门"
      /> -->
        <el-table-column label="使用" prop="is_used">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-select
                v-model="getParams.is_used"
                clearable
                placeholder=""
                @change="nameChanged" size="small"
              >
                <el-option
                  v-for="item in optionsUser"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.is_used ? 'Y' : 'N' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建人" prop="created_username">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.created_user" prefix-icon="el-icon-search" size="small" clearable @input="nameChanged" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_username?scope.row.created_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建时间">
          <el-table-column>
            <template slot="header" slot-scope="scope">
              <el-date-picker
                v-model="getParams.created_time"
                value-format="yyyy-MM-dd"
                type="date"
                placeholder=""
                @change="nameChanged" size="small"
              />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_time?scope.row.created_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column
          label="操作"
          width="150"
        >
          <template slot-scope="scope">
            <el-button-group>
              <el-button
                v-permission="['roles','change']"
                size="mini"
                type="text"
                @click="showEditGroupDialog(scope.row)"
              >修改
              </el-button>
              <!-- <el-button
              v-permission="['groupextension','delete']"
              size="mini"
              type="danger"
              plain
              @click="handleGroupDelete(scope.row)"
            >{{ scope.row.is_used?'停用':'启用' }}
            </el-button> -->
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page
        :old-page="false"
        :total="count"
        :current-page="getParams.page"
        @currentChange="changePage"
      />
    </el-footer>
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogEditGroupVisible"
      :close-on-click-modal="false"
      width="800px"
      :before-close="handleClose"
    >
      <el-form
        ref="groupForm"
        :model="groupForm"
      >
        <el-row>
          <el-col :span="12">
            <el-form-item
              :error="groupFormError.group_code"
              label="角色代码"
            >
              <el-input
                v-model="groupForm.group_code"
                disabled
              />
            </el-form-item>
          </el-col>
          <!-- <el-col :span="12">
            <el-form-item label="部门">
              <el-cascader
                v-model="groupForm.section"
                :options="optionsSection"
                :props="{ checkStrictly: true,value:'id' }"
                :disabled="dialogTitle==='编辑角色'"
                @change="changeSection"
              />
            </el-form-item>
          </el-col> -->
          <el-col :span="12">
            <el-form-item
              :error="groupFormError.name"
              label="角色名称"
            >
              <el-input v-model="groupForm.name" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="菜单筛选">
              <el-input
                v-model="permission_name"
                clearable
                @input="changeList"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <!-- <el-form-item
          :error="groupFormError.is_used"
          label="是否使用"
        >
          <el-switch v-model="groupForm.is_used" />
        </el-form-item> -->
        <el-form-item
          label="权限设置"
          size="medium"
        >
          <!-- :group-id="groupForm.id" -->
          <transferLimit
            ref="Permission"
            :view-section-permission="true"
            :section-id="departmentId"
            :default-permissions="groupForm.permissions"
            @changeTransferPermissions="changeTransferPermissions"
          />
        </el-form-item>
      </el-form>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button
          type="primary"
          @click="handleEditGroup('groupForm')"
        >确 定</el-button>
      </div>
    </el-dialog>
  </div>

</template>

<script>
import { sectionTree, roles, rolesUpdate, rolesDel } from '@/api/jqy'
import page from '@/components/page'
import transferLimit from './transferLimit'
import { checkPermission } from '@/utils/index'
import { commonCode } from '@/api/global-codes-manage'
import Cookies from 'js-cookie'

export default {
  name: 'GroupManage',
  components: { page, transferLimit },
  data() {
    return {
      getParams: {
        page: 1,
        is_used: null
      },
      tableData: [],
      count: 0,
      group_code: '',
      name: '',
      permission_name: '',
      groupForm: {
        name: '',
        group_code: '',
        is_used: true
      },
      groupFormError: {
        name: '',
        group_code: '',
        is_used: ''
      },
      permissions: [],
      dialogEditGroupVisible: false,
      dialogTitle: '新增角色',
      loading: true,
      loadingTable: false,
      optionsUser: [
        {
          value: 1,
          label: 'Y'
        },
        {
          value: 0,
          label: 'N'
        }
      ],
      currentVal: [],
      optionsSection: [],
      is_superuser: Cookies.get('is_superuser'),
      departmentId: ''
      // permission_section: JSON.parse(Cookies.get('permission_section'))
    }
  },
  computed: {
  },
  created() {
    this.currentChange()
  },
  mounted() {
    this.getOptionsSection()
  },
  methods: {
    checkPermission,
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    useFun(val) {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      const arr1 = []
      this.currentVal.forEach(d => {
        if (val === '禁用' && d.is_used) {
          arr.push(d.id)
        } else if (val === '启用' && !d.is_used) {
          arr.push(d.id)
        }
      })
      this.currentVal.forEach(d => {
        arr1.push(d.name)
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // userOperationLog('post', null, { data: { 'operator': Cookies.get('name_MCS'), 'menu_name': '角色管理', 'operations': val + '：' + arr1.join() + '角色' }})
        this.$store.dispatch('settings/operateTypeSetting', val)
        rolesUpdate('post', null, { data: { 'obj_ids': arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.nameChanged()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    deleteFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      const arr1 = []
      this.currentVal.forEach(d => {
        arr.push(d.id)
      })
      this.currentVal.forEach(d => {
        arr1.push(d.name)
      })
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', '删除')
        rolesDel('post', null, { data: { obj_ids: arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.nameChanged()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    currentChange() {
      this.loadingTable = true
      //   this.tableData = []
      roles('get', null, {
        params: this.getParams
      }).then(response => {
        this.loading = false
        this.loadingTable = false
        this.count = response.count || 0
        this.tableData = response.results || []
        // eslint-disable-next-line handle-callback-err
      }).catch(error => {
        this.loading = false
        this.loadingTable = false
      })
    },
    async getOptionsSection() {
      try {
        if (this.is_superuser === 'true') {
          const data = await sectionTree('get')
          if (data.results && data.results[0].children.length > 0) {
            this.optionsSection = data.results[0].children
            this.optionsSection = filterMy(this.optionsSection)
            this.optionsSection.forEach(d => {
              delete d.children
            })
          } else {
            this.optionsSection = []
          }
        } else {
          this.optionsSection = this.permission_section
          this.optionsSection.forEach(d => {
            d.label = d.name
          })
        }
      } catch (error) {
        //
      }
    },
    formatter: function(row, column) {
      return row.is_used ? 'Y' : 'N'
    },
    changePage(page, page_size) {
      this.getParams.page = page
      this.getParams.page_size = page_size
      this.currentChange()
    },
    groupCodeChanged() {
      this.getParams['page'] = 1
      this.currentChange()
    },
    nameChanged() {
      this.getParams['page'] = 1
      this.currentChange()
    },
    clearGroupForm() {
      this.groupForm = {
        name: '',
        group_code: '',
        is_used: true,
        section: ''
      }
      this.departmentId = ''
      this.permission_name = ''
    },
    clearGroupFormError() {
      this.groupFormError = {
        name: '',
        group_code: '',
        is_used: ''
      }
    },
    showCreateGroupDialog() {
      this.permission_name = null
      this.getCode(5)
      this.clearGroupForm()
      this.clearGroupFormError()
      this.dialogTitle = '新增角色'
      this.dialogEditGroupVisible = true
    },
    async getCode(num) {
      try {
        const { results } = await commonCode({ code: num })
        this.groupForm.group_code = results
      } catch (e) {
        //
      }
    },
    handleEditGroup() {
      this.clearGroupFormError()
      // if (!this.groupForm.section) {
      //   this.$message('请选择部门')
      //   return
      // }
      if (!this.groupForm.name) {
        this.$message('请填写角色名称')
        return
      }
      const type = this.groupForm.id ? 'put' : 'post'
      const id = this.groupForm.id ? this.groupForm.id : ''
      const obj = JSON.parse(JSON.stringify(this.groupForm))
      if (obj.section instanceof Array) {
        obj.section = obj.section[0]
      }
      if (this.groupForm.id) {
        this.$store.dispatch('settings/operateTypeSetting', '变更')
      } else {
        this.$store.dispatch('settings/operateTypeSetting', '新增')
      }
      roles(type, id, { data: { ...obj }})
        .then(response => {
          this.dialogEditGroupVisible = false
          this.$message.success(this.groupForm.name + this.groupForm.id ? '编辑成功' : '创建成功')
          this.groupForm.id = null
          this.currentChange()
          this.handleClose(false)
        }).catch()
    },
    showEditGroupDialog(group) {
      this.permission_name = null
      this.groupForm = JSON.parse(JSON.stringify(group))
      this.departmentId = this.groupForm.section
      this.clearGroupFormError()
      this.dialogTitle = '编辑角色'
      this.dialogEditGroupVisible = true
    },
    changeList() {
      if (this.permission_name !== '') {
        this.$refs['Permission'].permissionsData = this.$refs['Permission'].permissionsList.filter(d => { return (d.name.indexOf(this.permission_name) !== -1) })
      } else {
        this.$refs['Permission'].permissionsData = this.$refs['Permission'].permissionsList
      }
    },
    changeTransferPermissions(val) {
      this.$set(this.groupForm, 'permissions', val)
    },
    handleClose(done) {
      this.groupForm.id = null
      this.dialogEditGroupVisible = false
      this.departmentId = null
      if (done) {
        done()
      }
    },
    changeSection(val) {
      if (!val) {
        return
      }
      this.$set(this.groupForm, 'permissions', [])
      // 获取第二级id
      this.departmentId = val[0]
    }
  }
}
// 去掉最后一个空children
function filterMy(data) {
  const res = []
  data.forEach(D => {
    const tmp = {
      ...D
    }
    if (tmp.children.length > 0) {
      tmp.children = filterMy(tmp.children)
    } else {
      delete tmp.children
    }
    res.push(tmp)
  })
  return res
}
</script>
<style lang="scss">
  .roles-manage{
    .el-input{
      width:auto;
    }
    .el-transfer__buttons{
      padding: 0 15px;
    }
    .el-transfer-panel{
      width: 240px;
    }
    .el-checkbox{
      margin-right: 5px;
    }
  }
</style>
