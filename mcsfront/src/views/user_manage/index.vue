<template>
  <div v-loading="loading" class="userInfo">
    <!-- 用户管理 -->
    <div class="center-box">
      <div class="botton-box">
        <el-button v-permission="['users','add']" type="blue" icon="el-icon-plus" size="small" @click="showCreateUserDialog">新建</el-button>
        <!-- <el-button
          v-permission="['users','export']"
          type="blue"
          icon="el-icon-download"
          size="small"
          :loading="btnExportLoad"
          @click="templateDownload"
        >导出</el-button> -->
        <!-- <el-button
          v-permission="['personnels','export']"
          type="blue"
          icon="el-icon-download"
          size="small"
        >
          <a
            :href="`${templateFileUrl}user.xlsx`"
            download="用户管理导入模板.xlsx"
          >导出Excel模板</a>
        </el-button> -->
        <!-- <el-upload
          v-permission="['users','import']"
          style="margin-left:8px;display:inline-block"
          action="string"
          accept=".xls, .xlsx"
          :http-request="Upload"
          :show-file-list="false"
        >
          <el-button
            type="blue"
            size="small"
          >导入Excel</el-button>
        </el-upload> -->
        <el-button v-permission="['users','update']" style="margin-left:8px" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用')">禁用</el-button>
        <el-button v-permission="['users','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用')">启用</el-button>
        <el-button v-permission="['users','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <el-checkbox v-model="getParams.checked" style="margin-left:10px" @change="numChanged">按修改时间排序</el-checkbox>
      </div>
      <el-table v-loading="loadingTable" :data="tableData" tooltip-effect="dark" style="width: 100%;padding: 0 10px 0 10px;" stripe @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="40" />
        <el-table-column label="用户名" prop="username">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.username" prefix-icon="el-icon-search" size="small" clearable @input="numChanged" />
            </template>
            <template slot-scope="{row}">
              {{ row.username }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="部门" prop="department_name">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.department_name" clearable placeholder="" size="mini" @change="numChanged" @visible-change="visibleChange">
                <el-option v-for="item in sectionPick" :key="item.id" :label="item.name" :value="item.name" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.department_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="使用" prop="is_active">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.is_active" clearable placeholder="" size="small" @change="numChanged">
                <el-option v-for="item in optionsUser" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.is_active ? 'Y' : 'N' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建人">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.created_username" prefix-icon="el-icon-search" size="small" clearable @input="numChanged" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_username?scope.row.created_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建时间">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-date-picker size="small" v-model="getParams.created_time" value-format="yyyy-MM-dd" type="date" placeholder="" @change="numChanged" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_time?scope.row.created_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="修改人">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.last_update_username" prefix-icon="el-icon-search" size="small" clearable @input="numChanged" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.last_update_username?scope.row.last_update_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="修改时间">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.last_updated_time" type="date" size="small" value-format="yyyy-MM-dd" placeholder="" @change="numChanged" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.last_updated_time?scope.row.last_updated_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button-group>
              <el-button v-permission="['users','change']" size="mini" type="text" @click="showEditUserDialog(scope.row)">修改
              </el-button>
              <!-- <el-button
              size="mini"
              type="danger"
              plain
              @click="handleUserDelete(scope.row)"
            >
              {{ scope.row.is_active?'停用':'启用' }}
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="userDelete(scope.row)"
            >
              删除
            </el-button> -->
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="count" :current-page="getParams.page" @currentChange="changePage" />
    </el-footer>

    <el-dialog :title="userForm.id?'编辑用户':'新增用户'" :visible.sync="dialogCreateUserVisible" :before-close="handleClose" :close-on-click-modal="false" width="70%" style="min-width:900px">
      <el-form ref="userForm" :model="userForm" :rules="rules" label-width="100px" inline>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="userForm.id ? true:false" />
        </el-form-item>
        <!-- <el-form-item
          label="身份证"
          prop="id_card_num"
        >
          <el-input
            v-model="userForm.id_card_num"
            :disabled="userForm.id&&!card_num"
          />
          <el-button v-if="userForm.id" v-permission="['user','cid']" style="margin-left:20px" @click="card_num=true">修改身份证</el-button>
        </el-form-item> -->
        <el-form-item v-if="userForm.id" label="修改密码" prop="modifypassword">
          <el-input v-model="userForm.modifypassword" type="password" autocomplete="off" />
        </el-form-item>
        <el-form-item v-if="!userForm.id" label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" autocomplete="off" />
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass" :rules="{required: !userForm.id, validator: validatePass2, trigger: 'blur'}">
          <el-input v-model="userForm.checkPass" type="password" autocomplete="off" />
        </el-form-item>
        <el-form-item label="部门" :error="userFormError.department" prop="department">
          <el-cascader v-model="userForm.department" :options="optionsSection" :props="{ checkStrictly: true,value:'id' }" @change="changeSection" @visible-change="visibleChange1" />
        </el-form-item>
        <br>
        <el-form-item label="角色" size="medium">
          <transferRoles :default-groups="userForm.group_extensions" :groups="group_extensions" @changeTransferGroup="changeTransferGroup" />
        </el-form-item>
        <br>
        <el-form-item label="权限" size="medium" class="permissions-transfer">
          <transferLimit style="width:900px" :view-section-permission="true" :disable="dialogCreateUserVisible" :default-permissions="userForm.permissions" @changeTransferPermissions="changeTransferPermissions" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnloading" @click="handleCreateUser('userForm')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { delUser, userImport, personnelsUrl, sectionTree, roles, personnelsUrlDel } from '@/api/jqy'
import page from '@/components/page'
import { mapGetters } from 'vuex'
import transferLimit from './transferLimit'
import transferRoles from './transferRoles'
import Cookies from 'js-cookie'
export default {
  name: 'UserManage',
  components: { page, transferRoles, transferLimit },
  data() {
    var validatePass = (rule, value, callback) => {
      var reg = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).{8,}/
      if (!value) {
        callback(new Error('请输入密码'))
      } else if (value && !reg.test(value)) {
        callback(new Error('密码必须同时包含大写英文,小写英文,数字,符号,且不少于8位'))
      } else {
        if (this.userForm.checkPass !== '') {
          this.$refs.userForm.validateField('checkPass')
        }
        callback()
      }
    }
    this.validatePass2 = (rule, value, callback) => {
      if (this.userForm.id) {
        if (this.userForm.modifypassword && value !== this.userForm.modifypassword) {
          callback(new Error('两次输入密码不一致!'))
        } else {
          callback()
        }
      }
      if (!value) {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.userForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    var validatePass3 = (rule, value, callback) => {
      const _value = value.trim()
      if (!_value) {
        callback(new Error('请输入用户名!'))
      } else if (!/^[a-zA-Z0-9\u4e00-\u9fa5]+$/g.test(_value)) {
        callback(new Error('用户名格式错误，请输入字母或数字'))
      } else if (_value.length > 64) {
        callback(new Error('长度小于64个字符!'))
      } else if (_value.length < 2) {
        callback(new Error('请输入最少两个字符!'))
      } else {
        callback()
      }
    }
    var validatePass4 = (rule, value, callback) => {
      var reg = /(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[\W_]).{8,}/
      if (value && (!reg.test(value))) {
        callback(new Error('密码必须同时包含大写英文,小写英文,数字,符号,且不少于8位'))
      } else {
        callback()
      }
    }
    return {
      isError: false,
      isErrorOldPassword: false,
      titleOldPassword: '',
      titleNewPassword: true,
      btnloading: false,
      getParams: {
        page: 1,
        num: '',
        username: '',
        is_active: null
      },
      currentPage: 1,
      dialogCreateUserVisible: false,
      userForm: {
        username: '',
        password: '',
        department: null,
        checkPass: '',
        num: null,
        permission: [],
        group_extensions: []
      },
      tableData: [],
      count: 0,
      rules: {
        password: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        modifypassword: [
          { validator: validatePass4, trigger: 'blur' }
        ],
        username: [
          { required: true, validator: validatePass3, trigger: 'blur' }
        ],
        num: [
          { required: true, message: '请填写工号', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ]
      },
      group_extensions: [],
      loading: false,
      card_num: false,
      btnExportLoad: false,
      loadingTable: false,
      userFormError: {},
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
      sectionPick: [],
      teamList: [],
      is_superuser: Cookies.get('is_superuser'),
      departmentId: ''
      // permission_section: JSON.parse(Cookies.get('permission_section'))
    }
  },
  computed: {
    ...mapGetters(['permission'])
  },
  created() {
    this.permissionObj = this.permission
    this.loading = true
    // if (this.permissionObj.user.indexOf('change') > -1 ||
    //   this.permissionObj.user.indexOf('add') > -1) {
    // permissions('get', null).then(response => {
    //   const permissionsArr = response.results
    //   permissionsArr.forEach(D => {
    //     D.key = D.id
    //     D.label = D.name
    //   })
    //   this.permissionsArr = permissionsArr
    //   // eslint-disable-next-line handle-callback-err
    // }).catch(error => {
    // })
    // }
    this.currentChange()
    this.getOptionsSection()
    this.templateFileUrl = process.env.BASE_URL
  },
  methods: {
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
        if (val === '禁用' && d.is_active) {
          arr.push(d.id)
        } else if (val === '启用' && !d.is_active) {
          arr.push(d.id)
        }
      })
      this.currentVal.forEach(d => {
        arr1.push(d.username)
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', val)
        delUser('post', null, { data: { 'obj_ids': arr } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.numChanged()
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
        arr1.push(d.username)
      })
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', '删除')
        personnelsUrlDel('post', null, { data: { obj_ids: arr } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.numChanged()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    changeUsername(e) {
      this.userForm.username = e.target.value
    },
    blurUsername() {
      if (!this.userForm.username) {
        this.isError = true
      } else {
        this.isError = false
      }
    },
    changeOldPassword(e) {
      this.userForm.oldPassword = e.target.value
    },
    async getOptionsSection() {
      try {
        const data = await sectionTree('get')
        if (data.results && data.results[0].children.length > 0) {
          this.optionsSection = data.results[0].children
          this.optionsSection = filterMy(this.optionsSection)
        } else {
          this.optionsSection = []
        }
        // if (this.optionsSection.length && this.is_superuser === 'false') {
        //   // 不是系统管理员 过滤当前下的部门
        //   const arr = this.optionsSection.filter(d => { return (this.permission_section.findIndex(D => D.id === d.id)) > -1 })
        //   this.optionsSection = arr
        // }
        const data1 = await sectionTree('get', null, { params: { all: 1 } })
        this.sectionPick = data1.results
      } catch (error) {
        //
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getOptionsSection()
      }
    },
    async getGroupList() {
      try {
        // if (!this.departmentId) {
        //   return
        // }
        roles('get', null, {
          params: { all: 1 }
        }).then(response => {
          const groups = response
          groups.forEach(D => {
            D.key = D.id
            D.label = D.name
          })
          this.group_extensions = groups
        }).catch()
      } catch (error) {
        //
      }
    },
    visibleChange1(bool) {
      if (bool) {
        this.getOptionsSection()
      }
    },
    changeSection(val) {
      this.group_extensions = []
      this.departmentId = val ? val[0] : ''
      this.getGroupList()
    },
    currentChange() {
      const app = this
      if (!this.loading) {
        this.loadingTable = true
      }
      const obj = JSON.parse(JSON.stringify(this.getParams))
      if (!obj.is_superuser) {
        delete obj.is_superuser
      }
      personnelsUrl('get', null, {
        params: obj
      }).then((response) => {
        this.count = response.count || 0
        app.tableData = response.results || []
        this.loading = false
        this.loadingTable = false
        // eslint-disable-next-line handle-callback-err
      }).catch((error) => {
        this.loading = false
        this.loadingTable = false
      })
    },
    numChanged() {
      this.getParams.ordering = this.getParams.checked ? '-last_updated_time' : ''
      this.getParams['page'] = 1
      this.currentChange()
    },
    userNameChanged() { },
    showCreateUserDialog() {
      this.getGroupList()
      this.clearUserForm()
      if (this.$refs['userForm']) { this.$refs['userForm'].resetFields() }
      this.dialogCreateUserVisible = true
    },
    clearUserForm() {
      this.userForm = {
        username: '',
        password: '',
        checkPass: '',
        permission: []
      }
    },
    showEditUserDialog(row) {
      this.userForm = {
        department: null
      }
      personnelsUrl('get', row.id).then((response) => {
        this.userForm = response
        this.departmentId = response.factory_id
        this.getGroupList()
        this.dialogCreateUserVisible = true
      }).catch()
    },
    changePage(page, page_size) {
      this.getParams.page = page
      this.getParams.page_size = page_size
      this.currentChange()
    },
    handleCreateUser(formName) {
      var app = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // eslint-disable-next-line prefer-const
          let type = app.userForm.id ? 'put' : 'post'
          // eslint-disable-next-line prefer-const
          let paramsId = app.userForm.id ? app.userForm.id : ''
          if (app.userForm.id) {
            if (app.userForm.modifypassword) {
              app.userForm.password = app.userForm.modifypassword
            } else {
              delete app.userForm.password
            }
          }
          if (this.userForm.password === '') {
            delete app.userForm.password
          }
          if (this.userForm.num === '') {
            delete app.userForm.num
          }
          const obj = JSON.parse(JSON.stringify(app.userForm))
          if (obj.department && obj.department.length > 0 && obj.department instanceof Array) {
            obj.department = obj.department.slice(-1)[0]
          } else if (!obj.department || obj.department.length === 0) {
            obj.department = ''
          }
          this.btnloading = true
          if (app.userForm.id) {
            this.$store.dispatch('settings/operateTypeSetting', '变更')
          } else {
            this.$store.dispatch('settings/operateTypeSetting', '新增')
          }
          personnelsUrl(type, paramsId, { data: obj })
            .then((response) => {
              app.dialogCreateUserVisible = false
              app.$message.success(app.userForm.username + '操作成功')
              app.currentChange()
              app.handleClose(false)
              app.btnloading = false
            }).catch((e) => {
              this.userFormError = e
              this.btnloading = false
            })
        } else {
          return false
        }
      })
    },
    Upload(param) {
      const formData = new FormData()
      formData.append('file', param.file)
      userImport('post', null, { data: formData }).then(response => {
        this.$message({
          type: 'success',
          message: response
        })
        this.currentChange()
      })
    },
    templateDownload() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = personnelsUrl
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    },
    handleClose(done) {
      this.$refs['userForm'].resetFields()
      this.isError = false
      this.isErrorOldPassword = false
      this.departmentId = ''
      this.dialogCreateUserVisible = false
      if (done) {
        done()
      }
    },
    formatter: function(row, column) {
      return row.is_active ? 'Y' : 'N'
    },
    changeTransferGroup(val) {
      this.$set(this.userForm, 'group_extensions', val)
    },
    changeTransferPermissions(val) {
      this.$set(this.userForm, 'permissions', val)
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
.userInfo{
  .el-input{
    width:auto;
  }
  .el-transfer__buttons{
      padding: 0 15px;
    }
  // .permissions-transfer{
    .el-transfer-panel{
      width: 240px;
    }
    .el-checkbox{
      margin-right: 5px;
    }
  // }

    .show-enter-active{
       transition:all .9s;
    }
    .show-leave-active{
       transition:all .1s;
    }
    .show-enter,.show-leave{
        margin-top:1px;

    }
     .show-enter-to,.show-leave-to{
        margin-top: 1px;
   }
   .el-form-item__error{
    //  width: 170%;
    margin-left: -49px;
   }
}
</style>
