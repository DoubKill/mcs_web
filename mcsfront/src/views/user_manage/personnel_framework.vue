<template>
  <div class="personnel-framework">
    <!-- 人员组织架构 -->
    <el-container style="height:75vh;" class="container-style">
      <el-aside width="380px" class="border-style aside-style">
        <h3>部门管理</h3>
        <el-tree
          ref="tree"
          class="filter-tree"
          :highlight-current="true"
          :data="data"
          default-expand-all
          :props="defaultProps"
          :expand-on-click-node="false"
          node-key="id"
          @node-contextmenu="nodeContextmenu"
          @node-click="handleNodeClick"
        />
      </el-aside>
      <el-main v-loading="loading" class="border-style">
        <h3>人员</h3>
        <el-form :inline="true" label-width="68px">
          <el-form-item label="部门名称">
            <el-input v-model="formInline.label" style="width:200px" disabled />
          </el-form-item>
          <el-form-item label="负责人">
            <el-input v-model="formInline.in_charge_username" style="width:100px" disabled />
          </el-form-item>
          <!-- <el-form-item v-show="formInline.children&&formInline.children.length===0" label="负责区域">
            <el-select v-model="formInline.repair_areas" style="width:400px" multiple placeholder="请选择" @change="setRepairAreas">
              <el-option
                v-for="item in options"
                :key="item"
                :label="item"
                :value="item"
              />
            </el-select>
          </el-form-item> -->
          <!-- <el-form-item v-if="secondFloor&&is_superuser==='true'">
            <el-button type="primary" @click="showControl">本部门管控界面</el-button>
            <el-button type="primary" @click="showManage">本部门管理员设定</el-button>
          </el-form-item> -->
        </el-form>
        <el-table
          :data="tableData"
          stripe
        >
          <el-table-column
            align="center"
            type="index"
            label="序号"
            min-width="20"
          />
          <el-table-column
            prop="username"
            label="名字"
            min-width="20"
          />
        </el-table>
        <page
          :old-page="false"
          :total="total"
          :current-page="formInline.page"
          @currentChange="currentChange"
        />
      </el-main>
    </el-container>

    <ul v-show="visible" :style="{left:left+'px',top:top+'px'}" class="contextmenu">
      <li v-permission="['department','delete']" @click="delNodeFun">删除节点</li>
      <li v-permission="['department','change']" @click="setNodeFun(true)">修改节点</li>
      <li v-permission="['department','add']" @click="setNodeFun(false)">添加子节点</li>
    </ul>

    <el-dialog
      title="操作信息"
      :visible.sync="dialogVisible"
      width="400px"
      :before-close="handleClose"
    >
      <el-form ref="dialogForm" :model="dialogForm" :inline="true" label-width="100px" :rules="rules">
        <!-- <el-form-item label="部门编号" prop="section_id">
          <el-input v-model="dialogForm.section_id" :disabled="dialogForm.id?true:false" />
        </el-form-item> -->
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="dialogForm.name" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-select v-model="dialogForm.in_charge_user" filterable placeholder="请选择">
            <el-option
              v-for="item in userList"
              :key="item.id"
              :label="item.username"
              :value="item.id"
              :disabled="!item.is_active"
            >
              <span style="float: left">{{ item.username }}</span>
              <span v-if="!item.is_active" style="float: right;">{{ item.is_active?'':'已停用' }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="部门级管理员 管控范围设定"
      :visible.sync="dialogVisible1"
      width="1000px"
      :before-close="handleClose1"
    >
      <el-form inline>
        <el-form-item
          label="模块选择"
        >
          <el-select v-model="userForm.category_name" clearable placeholder="请选择">
            <el-option
              v-for="group in categoryList"
              :key="group"
              :label="group"
              :value="group"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="菜单">
          <el-input v-model="userForm.technology" clearable />
        </el-form-item>
        <el-form-item
          label="权限"
          size="medium"
        >
          <transferLimit
            style="width:900px"
            :is-export="true"
            :category="userForm.category_name"
            :menu="userForm.technology"
            :section-id="formInline.id"
            @changeTransferPermissions="changeTransferPermissions"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleClose1(false)">取 消</el-button>
        <el-button type="primary" :loading="btnloading" @click="handleCreateUser(1)">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="部门级 管理员设定"
      :visible.sync="dialogVisible2"
      width="600px"
      :before-close="handleClose2"
    >
      <el-form>
        <el-form-item
          label="本组织管理员（可多选）"
        >
          <userMangeSelect class="userMangeSelect" width-px="300px" :default-val="sampling_user" :is-multiple="true" :section-name="null" :is-created="true" :is-superuser="true" @changeSelect="changeSelectUser" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleClose2(false)">取 消</el-button>
        <el-button type="primary" :loading="btnloading" @click="createMangeUser">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import page from '@/components/page'
import { personnelsUrl, sectionTree } from '@/api/jqy'
import transferLimit from './transferLimit'
import userMangeSelect from './userMangeSelect'
import Cookies from 'js-cookie'
export default {
  name: 'EquipmentMasterDataPersonnelFramework',
  components: { page, transferLimit, userMangeSelect },
  data() {
    return {
      data: [],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      loading: false,
      left: '',
      top: '',
      visible: false,
      selectedTag: '',
      selectedTagParent: '',
      formInline: {
        repair_areas: []
      },
      tableData: [],
      total: 0,
      dialogVisible: false,
      dialogForm: {},
      btnLoading: false,
      userList: [],
      rules: {
        section_id: [{ required: true, message: '不能为空', trigger: 'blur' }],
        name: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      // options: [],
      secondFloor: '',
      is_superuser: Cookies.get('is_superuser'),
      permissionsArr: [],
      userForm: {},
      dialogVisible1: false,
      btnloading: false,
      sampling_user: [],
      dialogVisible2: false,
      permissionsRange: [],
      categoryList: ['基础信息管理', '工艺管理', '生产计划管理', '生产管理', '库存管理', '质量管理', '设备管理', '备品备件管理', '钉钉小程序']
    }
  },
  watch: {
    visible(value) {
      if (value) {
        document.body.addEventListener('click', this.closeMenu)
      } else {
        document.body.removeEventListener('click', this.closeMenu)
      }
    }
  },
  created() {
    this.getTree()
    // this.getResponsibleArea()
    this.getUserList(true)
  },
  methods: {
    async getTree() {
      try {
        const data = await sectionTree('get')
        this.data = data.results || []
        if (this.dialogForm.id && (this.formInline.id === this.dialogForm.id)) {
          this.$nextTick(d => {
            this.$refs.tree.setCurrentKey(this.dialogForm.id)
            this.formInline = this.$refs.tree.getCurrentNode()
          })
        } else {
          this.$nextTick(d => {
            this.$refs.tree.setCurrentKey(this.formInline.id)
          })
        }
      } catch (e) {
        //
      }
    },
    // async getResponsibleArea() {
    //   try {
    //     const data = await equipAreaDefine('get', null, { params: { all: 1 }})
    //     this.options = data
    //   } catch (e) {
    //     //
    //   }
    // },
    async setRepairAreas() {
      try {
        if (this.formInline.id) {
          const repair_areas = this.formInline.repair_areas.join(',')
          await sectionTree('patch', this.formInline.id, { data: { repair_areas }})
          this.$message.success('设置成功')
        }
      } catch (e) {
        //
      }
    },
    getPermission() {
      // permissions('get', null).then(response => {
      //   const permissionsArr = response.results
      //   permissionsArr.forEach(D => {
      //     D.key = D.id
      //     D.label = D.name
      //   })
      //   this.permissionsArr = permissionsArr
      // }).catch()
    },
    handleNodeClick(row) {
      this.closeMenu()
      this.formInline = row
      if (!this.formInline.repair_areas) {
        this.formInline.repair_areas = []
      } else {
        if (typeof this.formInline.repair_areas === 'string') {
          this.formInline.repair_areas = this.formInline.repair_areas.split(',')
        }
      }
      this.getUserList()
      this.secondFloor = this.data[0].children.some(d => d.id === row.id)
    },
    async getUserList(bool) {
      try {
        let obj = { department_name: this.formInline.label, is_active: 1,
          page: this.formInline.page,
          page_size: this.formInline.page_size }
        if (bool) {
          obj = { all: 1 }
        }
        this.loading = true
        const data = await personnelsUrl('get', null, { params: obj })
        if (bool) {
          this.userList = data || []
        } else {
          this.tableData = data.results || []
          this.total = data.count
        }
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.dialogForm = {}
      this.$refs.dialogForm.clearValidate()
      if (done) {
        done()
      }
    },
    currentChange(page, pageSize) {
      this.formInline.page = page
      this.formInline.page_size = pageSize
      this.getUserList()
    },
    nodeContextmenu(e, tag, node, event) {
      const menuMinWidth = 105
      const offsetLeft = this.$el.getBoundingClientRect().left // container margin left
      const offsetWidth = this.$el.offsetWidth // container width
      const maxLeft = offsetWidth - menuMinWidth // left boundary
      const left = e.clientX - offsetLeft + 40 // 15: margin right

      if (left > maxLeft) {
        this.left = maxLeft
      } else {
        this.left = left
      }

      this.top = e.clientY - 100
      this.visible = true
      this.selectedTag = tag
      this.selectedTagParent = node.parent.data
    },
    closeMenu() {
      this.visible = false
    },
    delNodeFun() {
      this.$confirm('是否确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('settings/operateTypeSetting', '删除')
        sectionTree('delete', this.selectedTag.id)
          .then(response => {
            this.$message({
              type: 'success',
              message: '删除成功!'
            })
            this.getTree()
            if (this.selectedTag.id && (this.formInline.id === this.selectedTag.id)) {
              this.formInline = {}
              this.tableData = []
              this.total = 0
            }
          }).catch(e => {
            this.$message.error('删除失败')
          })
      })
    },
    setNodeFun(bool) {
      this.dialogVisible = true
      if (bool) {
        this.dialogForm = {
          section_id: this.selectedTag.section_id,
          name: this.selectedTag.label,
          in_charge_user: this.selectedTag.in_charge_user_id,
          id: this.selectedTag.id
        }
      } else {
        this.dialogForm = {}
      }
    },
    submitFun() {
      this.$refs.dialogForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.dialogForm.id ? 'put' : 'post'
            if (!this.dialogForm.id) {
              this.dialogForm.parent_section = this.selectedTag.id || null
            }
            if (this.dialogForm.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await sectionTree(_api, this.dialogForm.id || null, { data: this.dialogForm })
            this.$message.success('操作成功')
            this.getTree()
            this.btnLoading = false
            this.dialogVisible = false
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    // showControl() {
    //   this.dialogVisible1 = true
    //   this.getPermission()
    // },
    // async showManage() {
    //   try {
    //     // 获取默认的管理员
    //     const data = await sectionTree('get', this.formInline.id, { params: { }})
    //     this.sampling_user = data.permission_user
    //   } catch (e) {
    //     //
    //   }
    //   this.dialogVisible2 = true
    // },
    async handleCreateUser(type) {
      try {
        let val = ''
        let obj = {}
        if (type === 1) {
          val = '管控范围设定设置成功'
          obj = { permissions: this.permissionsRange }
        } else {
          val = '管理员设定设置成功'
          obj = { permission_user: this.sampling_user }
        }
        await sectionTree('patch', this.formInline.id, { data: obj })
        this.$message.success(val)
        this.handleClose1(false)
        this.handleClose2(false)
      } catch (e) {
        //
      }
    },
    handleClose1(done) {
      this.dialogVisible1 = false
      this.userForm = {}
      if (done) {
        done()
      }
    },
    changeTransferPermissions(val) {
      this.permissionsRange = val
    },
    changeSelectUser(obj) {
      this.sampling_user = obj
    },
    handleClose2(done) {
      this.dialogVisible2 = false
      this.sampling_user = []
      if (done) {
        done()
      }
    },
    createMangeUser() {
      if (!this.sampling_user || !this.sampling_user.length) {
        this.$message('请选择本部门管理员')
        return
      }
      this.handleCreateUser(2)
    }
  }
}
</script>

<style lang="scss" scoped>
.personnel-framework{
  .container-style{
  ::-webkit-scrollbar {
    width: 1px;
  }
  }
  ::-webkit-scrollbar-thumb {
      background: #eee
  }
  .el-main{
    padding:0;
  }
  .border-style{
    border:1px solid #eee;
    padding-left:10px;
  }
  .aside-style{
    // padding: 20px;
    margin-right:10px;
  }
  .el-input{
    width:250px;
  }
   .contextmenu {
    margin: 0;
    background: #fff;
    z-index: 3000;
    position: absolute;
    list-style-type: none;
    padding: 5px 0;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 400;
    color: #333;
    box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, .3);
    li {
      margin: 0;
      padding: 7px 16px;
      cursor: pointer;
      &:hover {
        background: #eee;
      }
    }
  }
}
</style>
