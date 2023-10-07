<template>
  <div class="device_manage">
    <!-- 设备管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="设备">
          <el-input v-model="getParams.search" size="small" clearable placeholder="请输入设备名或者编码" />
        </el-form-item>
        <el-form-item label="设备类型">
          <el-select
            v-model="getParams.equip_type"
            size="small"
            clearable
            placeholder="请选择"
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="工序">
          <el-select
            v-model="getParams.process"
            clearable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="启用状态">
          <el-select
            v-model="getParams.is_used"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'已启用'},{id:false,name:'已禁用'}]"
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
        <el-button v-permission="['equips','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['equips','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['equips','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['equips','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          prop="equip_code"
          label="设备编码"
          min-width="20"
        />
        <el-table-column
          prop="equip_name"
          label="设备名称"
          min-width="20"
        />
        <el-table-column
          prop="equip_desc"
          label="设备描述"
          min-width="20"
        />
        <el-table-column
          prop="equip_type_name"
          label="设备类型"
          min-width="20"
        />
        <el-table-column
          prop="process_name"
          label="工序"
          min-width="20"
        />
        <!-- <el-table-column
          prop="ply_nums"
          label="缓存层数"
          min-width="20"
        /> -->
        <el-table-column
          label="启用状态"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'已启用':'已禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="wcs_code"
          label="WCS编号"
          min-width="20"
        />
        <el-table-column
          prop="client_code"
          label="客户端编号"
          min-width="20"
        />
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button v-permission="['equips','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
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
      :title="(currentObj.id?'编辑':'新建')+'设备信息'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="设备编号" prop="equip_code">
          <el-input v-model="currentObj.equip_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="设备名称" prop="equip_name">
          <el-input v-model="currentObj.equip_name" size="small" />
        </el-form-item>
        <el-form-item label="设备类型" prop="equip_type">
          <el-select
            v-model="currentObj.equip_type"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="设备描述">
          <el-input v-model="currentObj.equip_desc" size="small" />
        </el-form-item>
        <el-form-item label="工序" prop="process">
          <el-select
            v-model="currentObj.process"
            clearable
            size="small"
            placeholder="请选择"
            style="width:190px"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.process_name }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="缓存层数">
          <el-input-number v-model="currentObj.ply_nums" style="width:auto" size="small" controls-position="right" :min="0" />
        </el-form-item> -->
        <el-form-item label="WCS编号">
          <el-input v-model="currentObj.wcs_code" size="small" />
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
import { basicsEquips, basicsEquipsUpdate, basicsEquipsDel, productionProcesses } from '@/api/base_w'
// import { deviceTypes } from '@/api/base_w'
// import { getGlobalCodes } from '@/api/basics'
import page from '@/components/page'
export default {
  name: 'DeviceManage',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: { },
      dialogVisible: false,
      rules: {
        equip_code: [
          { required: true, message: '请填写设备编号', trigger: 'blur' }
        ],
        equip_name: [
          { required: true, message: '请填写设备名称', trigger: 'blur' }
        ],
        equip_type: [
          { required: true, message: '请选择设备类型', trigger: 'change' }
        ],
        process: [
          { required: true, message: '请选择工序', trigger: 'change' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      device_list: [
        { id: 1, global_name: '工序设备' },
        { id: 2, global_name: '缓存设备' }
      ],
      process_list: []
    }
  },
  created() {
    this.getList()
  },
  mounted() {},
  methods: {
    async getOtherList() {
      try {
        const a = await Promise.all([
          // getGlobalCodes({ all: 1, type_name: '设备类型' }),
          productionProcesses('get', null, { params: { all: 1 }})
        ])
        // this.device_list = a[0] || []
        this.process_list = a[0] || []
      } catch (e) {
        //
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getOtherList()
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await basicsEquips('get', null, { params: this.getParams })
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
      this.getOtherList()
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
        basicsEquipsDel('post', null, { data: { obj_ids: arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', '删除')
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
        basicsEquipsUpdate('post', null, { data: { 'obj_ids': arr }})
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
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
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            // if (!this.currentObj.ply_nums) {
            //   this.currentObj.ply_nums = 0
            // }
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await basicsEquips(_api, this.currentObj.id || null, { data: this.currentObj })
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
    }
  }
}
</script>

  <style lang="scss">
  .device_manage{
    .el-dialog__body .el-input--small .el-input__inner{
      width: 190px;
    }
  }

  </style>

