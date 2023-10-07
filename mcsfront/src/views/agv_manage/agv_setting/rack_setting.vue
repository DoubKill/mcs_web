<template>
  <div>
    <!--  货架设置 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="货架号">
          <el-input v-model="getParams.shelve_code" size="small" clearable placeholder="货架号" style="width:120px" />
        </el-form-item>
        <el-form-item label="起点">
          <el-select
            v-model="getParams.start_point"
            style="width:140px"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="终点">
          <el-select
            v-model="getParams.end_point"
            style="width:140px"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="工段"> <!-- × -->
          <el-select
            v-model="getParams.process"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in []"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="满篮">
          <el-select
            v-model="getParams.is_full"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'是'},{id:false,name:'否'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="在线"> <!-- × -->
          <el-select
            v-model="getParams.process"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in []"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="位置OK">
          <el-select
            v-model="getParams.is_valid"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in []"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态"><!-- √ -->
          <el-select
            v-model="getParams.shelve_state"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in stateList"
              :key="item.id"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物料标识"> <!-- √ -->
          <el-select
            v-model="getParams.material_identify_code"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in ItemIDList"
              :key="item.id"
              :label="item.identify_code"
              :value="item.identify_code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物料类别"><!-- √ -->
          <el-select
            v-model="getParams.material_type"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in materialCategory"
              :key="item.id"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="货架超时"><!-- × -->
          <el-select
            v-model="getParams.process"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in []"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="来源机台">
          <el-select
            v-model="getParams.original_equip_line_code"
            size="small"
            placeholder="请选择"
            clearable
            style="width:140px"
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="modify" icon="el-icon-download" size="small" :loading="btnExportLoad" @click="exportFun">导出</el-button>
        <el-upload
          style="margin:0 8px;display:inline-block"
          action="string"
          accept=".xls, .xlsx"
          :http-request="Upload"
          :show-file-list="false"
        >
          <el-button type="warning" size="small">导入Excel</el-button>
        </el-upload>
        <el-button type="success" icon="el-icon-caret-right" size="small" @click="searchFun">检索接口</el-button>
        <el-button type="danger" icon="el-icon-view" size="small" @click="logViewFun">日志查看</el-button>
      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <!-- @selection-change="handleSelectionChange" -->
        <!-- <el-table-column
          type="selection"
          width="40"
        /> -->
        <el-table-column
          label="货架号"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.shelve_code }}</template>
        </el-table-column>
        <el-table-column
          prop="time_consume"
          label="时间s"
          width="60"
        />
        <el-table-column
          prop="shelve_state"
          label="货架状态"
          min-width="20"
        />
        <el-table-column
          label="当前位置"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.current_location }}</template>
        </el-table-column>
        <el-table-column
          prop="is_valid"
          label="位置有效"
          min-width="20"
        />
        <el-table-column
          prop="material_type"
          label="物料类型"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="original_equip_line_code"
          label="来源机台"
          min-width="20"
        />
        <el-table-column
          prop="material_identify_code"
          label="物料标识"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="material_level"
          label="物料等级"
          show-overflow-tooltip
          min-width="20"
        />

        <el-table-column
          label="满篮"
          width="60"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_full?'':'info'">{{ scope.row.is_full?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="排除"
          width="60"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_eliminate?'':'info'">{{ scope.row.is_eliminate?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="start_point"
          label="起点"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="end_point"
          label="终点"
          min-width="20"
        />
        <el-table-column
          prop="task_no"
          label="任务号"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="going_equip_line_code"
          label="去向机台"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="target_equip_line_code"
          label="目标机台"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column label="操作" width="50">
          <template slot-scope="{row}">
            <el-button size="small" type="text" @click="editShow(row)">修改</el-button>
            <!-- <el-button size="small" type="text" @click="viewFun(row)">查看</el-button> -->
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
      width="700px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="110px" inline>
        <el-form-item label="货架号" prop="shelve_code">
          <el-input v-model="currentObj.shelve_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="时间s">
          <el-input-number v-model="currentObj.time_consume" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="货架状态">
          <el-select
            v-model="currentObj.shelve_state"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in stateList"
              :key="item.id"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="当前位置">
          <el-select
            v-model="currentObj.current_location"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="位置有效">
          <el-select
            v-model="currentObj.is_valid"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'是'},{id:false,name:'否'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物料类别">
          <el-select
            v-model="currentObj.material_type"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in materialCategory"
              :key="item.id"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="来源机台">
          <el-select
            v-model="currentObj.original_equip_line_code"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物料标识">
          <el-select
            v-model="currentObj.material_identify_code"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in ItemIDList"
              :key="item.id"
              :label="item.identify_code"
              :value="item.identify_code"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物料等级">
          <el-select
            v-model="currentObj.material_level"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in levelList"
              :key="item.id"
              :label="item.global_name"
              :value="item.global_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="满篮">
          <el-select
            v-model="currentObj.is_full"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'是'},{id:false,name:'否'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="排除">
          <el-select
            v-model="currentObj.is_eliminate"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'是'},{id:false,name:'否'}]"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="起点">
          <el-select
            v-model="currentObj.start_point"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="终点">
          <el-select
            v-model="currentObj.end_point"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.device_name"
              :value="item.device_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="任务号">
          <el-input v-model="currentObj.task_no" size="small" disabled />
        </el-form-item>
        <el-form-item label="去向机台">
          <el-select
            v-model="currentObj.going_equip_line_code"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in equipLine_list"
              :key="item.id"
              :label="item.line_name"
              :value="item.line_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="目标机台">
          <el-select
            v-model="currentObj.target_equip_line_code"
            size="small"
            placeholder="请选择"
            clearable
          >
            <el-option
              v-for="item in equipLine_list"
              :key="item.id"
              :label="item.line_name"
              :value="item.line_name"
            />
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
import { shelvesInfos, shelvesInfosImportXlsx, deviceInfos, equipLines } from '@/api/base_w'
import { materialIdentifies } from '@/api/jqy'
import { getGlobalCodes } from '@/api/basics'
import page from '@/components/page'
export default {
  name: 'RackSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        shelve_code: [
          { required: true, message: '请填写货架号', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      btnExportLoad: false,
      stateList: [],
      ItemIDList: [],
      levelList: [],
      materialCategory: [],
      device_list: [],
      equipLine_list: []
    }
  },
  created() {
    this.getList()
    this.getAllList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await shelvesInfos('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getAllList() {
      try {
        const a = await Promise.all([
          getGlobalCodes({ all: 1, type_name: '货架状态' }),
          getGlobalCodes({ all: 1, type_name: '物料类别' }),
          materialIdentifies('get', null, { params: { all: 1 }}),
          getGlobalCodes({ all: 1, type_name: '物料等级' }),
          deviceInfos('get', null, { params: { all: 1 }}),
          equipLines('get', null, { params: { all: 1 }})
        ])
        this.stateList = a[0] || []
        this.materialCategory = a[1] || []
        this.ItemIDList = a[2] || []
        this.levelList = a[3] || []
        this.device_list = a[4] || []
        this.equipLine_list = a[5] || []
      } catch (e) {
        //
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    changeList() {
      this.getParams.page = 1
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
    addFun() {
      this.dialogVisible = true
    },
    submitFun() {
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            await shelvesInfos(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.handleClose(null)
            this.changeList()
            this.btnLoading = false
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    searchFun() {},
    logViewFun() {},
    viewFun() {},
    Upload(param) {
      const formData = new FormData()
      formData.append('file', param.file)
      shelvesInfosImportXlsx('post', null, { data: formData }).then(response => {
        this.$message({
          type: 'success',
          message: response
        })
        this.changeList()
      })
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = shelvesInfos
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    }
  }
}
</script>

  <style lang="scss" scoped>
  .el-dialog__body .el-input--small{
    width: 192px !important;
  }
  </style>

