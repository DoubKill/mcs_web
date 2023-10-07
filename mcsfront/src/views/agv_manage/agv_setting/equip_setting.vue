<template>
  <div>
    <!-- 机台设置 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="机台号">
          <el-input v-model="getParams.device_code" size="small" clearable placeholder="机台号" />
        </el-form-item>
        <el-form-item label="机台类型">
          <el-select
            v-model="getParams.device_type_name"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.type_name"
              :value="item.type_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="getList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <!-- <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button> -->
        <el-button type="success" icon="el-icon-download" size="small" @click="exportFun">导出</el-button>
        <!-- <el-upload
          style="margin:0 8px;display:inline-block"
          action="string"
          accept=".xls, .xlsx"
          :http-request="Upload"
          :show-file-list="false"
        >
          <el-button type="warning" size="small">导入Excel</el-button>
        </el-upload> -->

        <el-button type="danger" icon="el-icon-turn-off" size="small" @click="deleteFun('禁用',1)">禁用</el-button>
        <el-button type="modify" icon="el-icon-open" size="small" @click="deleteFun('启用',1)">启用</el-button>
        <el-button type="danger" icon="el-icon-lock" size="small" @click="deleteFun('锁定',2)">锁定</el-button>
        <el-button type="modify" icon="el-icon-unlock" size="small" @click="deleteFun('解锁',2)">解锁</el-button>
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
          prop="device_code"
          label="机台号"
          min-width="20"
        />
        <el-table-column
          prop="device_name"
          label="机台名称"
          min-width="20"
        />
        <el-table-column
          prop="current_shelve_code"
          label="当前货架"
          min-width="20"
        />
        <el-table-column
          label="禁用"
          width="60"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_forbidden?'success':'info'">{{ scope.row.is_forbidden?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="急停"
          width="50"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_stop?'success':'info'">{{ scope.row.is_stop?'Yes':'No' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="锁定"
          width="60"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_locked?'':'info'">{{ scope.row.is_locked?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="locked_shelve_code"
          label="锁定货架"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="special_mode"
          label="特殊模式"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          label="启用专属休息区"
          min-width="20"
          show-overflow-tooltip
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_use_exclusive_rest_area?'':'info'">{{ scope.row.is_use_exclusive_rest_area?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="启用类别调度"
          min-width="20"
          show-overflow-tooltip
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_use_class_scheduling?'':'info'">{{ scope.row.is_use_class_scheduling?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="input_type"
          label="进料类别"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="output_type"
          label="出料类别"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="rest_area_code"
          label="休息区域"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="exclusive_rest_area_code"
          label="专属休息区"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="general_rest_area_code"
          label="普通休息区"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="target_equip_line"
          label="优先机台"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="setting_line_codes"
          label="机台去向"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button size="small" type="text" @click="editShow(row)">修改</el-button>
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
      :title="currentObj.id?'编辑':'新建'"
      :visible.sync="dialogVisible"
      width="750px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="机台号" prop="device_code">
          <el-input v-model="currentObj.device_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="机台名称" prop="device_name">
          <el-input v-model="currentObj.device_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="进料类型">
          <el-select
            v-model="currentObj.input_type"
            size="small"
            placeholder="请选择"
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in input_type_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="出料类型">
          <el-select
            v-model="currentObj.output_type"
            size="small"
            placeholder="请选择"
            :disabled="currentObj.id?true:false"
          >
            <el-option
              v-for="item in output_type_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="优先机台">
          <el-input v-model="currentObj.target_equip_line" :disabled="currentObj.id?true:false" size="small" />
        </el-form-item>
        <el-form-item label="机台去向">
          <el-input v-model="currentObj.setting_line_codes" :disabled="currentObj.id?true:false" size="small" />
        </el-form-item>
        <el-form-item label="货架号">
          <el-input v-model="currentObj.current_shelve_code" size="small" />
        </el-form-item>
        <el-form-item label="是否禁用">
          <el-radio v-model="currentObj.is_forbidden" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_forbidden" :label="false">否</el-radio>
        </el-form-item><br>
        <el-form-item label="是否急停">
          <el-radio v-model="currentObj.is_stop" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_stop" :label="false">否</el-radio>
        </el-form-item><br>
        <el-form-item label="是否锁定">
          <el-radio v-model="currentObj.is_locked" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_locked" :label="false">否</el-radio>
        </el-form-item><br>
        <el-form-item label="锁定货架">
          <el-input v-model="currentObj.locked_shelve_code" size="small" />
        </el-form-item>
        <el-form-item label="特殊模式">
          <el-input v-model="currentObj.special_mode" size="small" />
        </el-form-item>
        <el-form-item label="休息区域编号">
          <el-input v-model="currentObj.rest_area_code" size="small" />
        </el-form-item>
        <el-form-item label="专属休息区域编号">
          <el-input v-model="currentObj.exclusive_rest_area_code" size="small" />
        </el-form-item>
        <el-form-item label="普通休息区域编号">
          <el-input v-model="currentObj.general_rest_area_code" size="small" />
        </el-form-item>
        <el-form-item label="是否启用专属休息区">
          <el-radio v-model="currentObj.is_use_exclusive_rest_area" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_use_exclusive_rest_area" :label="false">否</el-radio>
        </el-form-item>
        <el-form-item label="是否启用类别调度">
          <el-radio v-model="currentObj.is_use_class_scheduling" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_use_class_scheduling" :label="false">否</el-radio>
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
import { deviceInfoSettings, deviceInfoSettingsBatchUpdate, deviceTypes } from '@/api/base_w'
import { getGlobalCodes } from '@/api/basics'
import page from '@/components/page'
export default {
  name: 'EquipSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        device_code: [
          { required: true, message: '请填写机台号', trigger: 'blur' }
        ],
        device_name: [
          { required: true, message: '请填写机台名称', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      input_type_list: [],
      output_type_list: [],
      device_list: []
    }
  },
  created() {
    this.getList()
    this.getCode()
  },
  mounted() {
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await deviceInfoSettings('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getCode() {
      try {
        const p = await Promise.all([getGlobalCodes({ all: 1, type_name: '进料类型' }), getGlobalCodes({ all: 1, type_name: '出料类型' }),
          deviceTypes('get', null, { params: { all: 1 }})])
        this.input_type_list = p[0] || []
        this.output_type_list = p[1] || []
        this.device_list = p[2] || []
      } catch (e) {
        //
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
      this.currentObj.input_type = this.currentObj.input_type.toString() || ''
      this.currentObj.output_type = this.currentObj.output_type.toString() || ''
      this.dialogVisible = true
    },
    resetFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
    },
    synchroFun() {},
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
    deleteFun(val, bool) {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      this.currentVal.forEach(d => {
        if (val === '禁用' && !d.is_forbidden) {
          arr.push(d.id)
        } else if (val === '启用' && d.is_forbidden) {
          arr.push(d.id)
        } else if (val === '锁定' && !d.is_locked) {
          arr.push(d.id)
        } else if (val === '解锁' && d.is_locked) {
          arr.push(d.id)
        }
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deviceInfoSettingsBatchUpdate('post', null, { data: { 'operation_type': bool, 'obj_ids': arr }})
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
            await deviceInfoSettings(_api, this.currentObj.id || null, { data: this.currentObj })
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
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = deviceInfoSettings
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    },
    Upload(param) {
      const formData = new FormData()
      formData.append('file', param.file)
      // shelvesInfosImportXlsx('post', null, { data: formData }).then(response => {
      //   this.$message({
      //     type: 'success',
      //     message: response
      //   })
      //   this.changeList()
      // })
    }
  }
}
</script>

  <style lang="scss" scoped>
.dialog-style{
    .el-select{
        width: 178px;
    }
}
  </style>

