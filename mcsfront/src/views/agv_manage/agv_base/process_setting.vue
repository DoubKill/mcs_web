<template>
  <div class="process_setting">
    <!-- 工艺段配置 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['process','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <!-- <el-upload
          v-permission="['process','import']"
          style="margin:0 8px;display:inline-block"
          action="string"
          accept=".xls, .xlsx"
          :http-request="Upload"
          :show-file-list="false"
        >
          <el-button type="blue" size="small">导入Excel</el-button>
        </el-upload> -->
        <el-button v-permission="['process','export']" type="blue" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
        <el-button v-permission="['process','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <el-button type="blue" size="small" @click="showDialog">工艺循环图</el-button>
      </div>
      <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" style="width: 100%" stripe @selection-change="handleSelectionChange" @sort-change="arraySpanMethod">
        <el-table-column type="selection" width="40" />
        <el-table-column label="工艺段ID" prop="process_ID" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.process_ID" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.process_ID }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="工艺段名称" prop="process_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.process_name" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.process_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column label="工艺段编号" prop="process_code" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.process_code" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.process_code }}
            </template>
          </el-table-column>
        </el-table-column> -->
        <el-table-column label="工艺段顺序" prop="ordering" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.ordered" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.ordering }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="源工艺段" prop="source_process_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.source_process_name" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.source_process_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="目标工艺段" prop="target_process_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.target_process_name" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.target_process_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column label="车间号" prop="workshop_no" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.workshop_no" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.workshop_no }}
            </template>
          </el-table-column>
        </el-table-column> -->
        <el-table-column label="工作区" prop="working_area_name" sortable="custom">
          <el-table-column min-width="20">
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
        <el-table-column label="上层轨道上下料类型" prop="upper_rail_type_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.upper_rail_type" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in railType_list" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.upper_rail_type_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="上层花篮类型" prop="upper_basket_type_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.upper_basket_type" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in basketType_list" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.upper_basket_type_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="下层轨道上下料类型" prop="lower_rail_type_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.lower_rail_type" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in railType_list" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.lower_rail_type_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="下层花篮类型" prop="lower_basket_type_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.lower_basket_type" size="small" placeholder="" clearable @change="changeList">
                <el-option v-for="item in basketType_list" :key="item.id" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.lower_basket_type_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="单轴花篮数量" prop="single_slot_num" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.single_slot_num" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.single_slot_num }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="单车电池片数量" prop="cell_numbers" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.cell_numbers" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.cell_numbers }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="物料超时时间(秒)" prop="q_time" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.q_time" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.q_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="QTime预警时间(秒)" prop="warning_time" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.warning_time" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.warning_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="节拍(秒)" prop="pitch_time" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.pitch_time" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.pitch_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button v-permission="['process','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>

    <el-dialog :title="currentObj.id?'编辑':'新建'" :visible.sync="dialogVisible" width="800px" :before-close="handleClose" class="dialog-style">
      <el-form ref="ruleForm" inline :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="工艺段ID" prop="process_ID">
          <el-input v-model="currentObj.process_ID" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <!-- <el-form-item label="工艺段编号" prop="process_code">
          <el-input v-model="currentObj.process_code" size="small" :disabled="currentObj.id?true:false" @input="writeId" />
        </el-form-item> -->
        <el-form-item label="工艺段名称" prop="process_name">
          <el-input v-model="currentObj.process_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="工艺段顺序" prop="ordering">
          <el-input-number v-model="currentObj.ordering" style="width:200px" size="small" controls-position="right" :min="1" :max="99" @change="writeId" />
        </el-form-item>
        <el-form-item v-if="currentObj.id?true:false" label="源工艺段" prop="source_process">
          <el-select v-model="currentObj.source_process" size="small" placeholder="请选择" clearable>
            <el-option v-for="item in process_list" :key="item.id" :label="item.process_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="currentObj.id?true:false" label="目标工艺段" prop="target_process">
          <el-select v-model="currentObj.target_process" size="small" placeholder="请选择" clearable>
            <el-option v-for="item in process_list" :key="item.id" :label="item.process_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <!-- <el-form-item
          label="车间号"
          prop="workshop_no"
        >
          <el-input
            v-model="currentObj.workshop_no"
            disabled
            size="small"
          />
        </el-form-item> -->
        <el-form-item label="工作区" prop="working_area">
          <el-select v-model="currentObj.working_area" size="small" placeholder="请选择">
            <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="上层轨道上下料类型">
          <el-select v-model="currentObj.upper_rail_type" size="small" clearable @change="writeId" placeholder="" :disabled="currentObj.id?true:false">
            <el-option v-for="item in railType_list" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="上层花篮类型" prop="upper_basket_type">
          <el-select v-model="currentObj.upper_basket_type" :disabled="!currentObj.upper_rail_type||currentObj.id?true:false" size="small" placeholder="" clearable>
            <el-option v-for="item in basketType_list" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="下层轨道上下料类型" prop="lower_rail_type">
          <el-select placeholder="" v-model="currentObj.lower_rail_type" :disabled="currentObj.id?true:false" size="small" clearable @change="writeId">
            <el-option v-for="item in railType_list" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="下层花篮类型" prop="lower_basket_type">
          <el-select v-model="currentObj.lower_basket_type" :disabled="!currentObj.lower_rail_type||currentObj.id?true:false" size="small" placeholder="" clearable>
            <el-option v-for="item in basketType_list" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="单车电池片数量" prop="cell_numbers">
          <el-input-number v-model="currentObj.cell_numbers" style="width:200px" size="small" controls-position="right" :min="1" />
        </el-form-item>
        <el-form-item label="物料超时时间(秒)" prop="q_time">
          <el-input-number v-model="currentObj.q_time" style="width:200px" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="QTime预警时间(秒)" prop="warning_time">
          <el-input-number v-model="currentObj.warning_time" style="width:200px" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="节拍(秒)" prop="pitch_time">
          <el-input-number v-model="currentObj.pitch_time" style="width:200px" size="small" controls-position="right" :min="1" />
        </el-form-item>
        <el-form-item label="单轴花篮数量" prop="single_slot_num">
          <el-input-number v-model="currentObj.single_slot_num" style="width:200px" size="small" controls-position="right" :min="1" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="工艺循环图" :visible.sync="dialogVisible1" width="800px">
      <div v-for="(item,i) in cyclicGraphList" :key="item.work_area">
        <div :id="'taskLine'+i" class="volumeBox" style="width: 100%;height:400px;" />
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from '@/utils'
import common from '@/utils/common'
import { workAreas, processCyclicGraph } from '@/api/base_w'
import { processSections, processSectionsDel, processSectionsImport } from '@/api/jqy'
import page from '@/components/page'
import * as echarts from 'echarts'
export default {
  name: 'ProcessSetting',
  components: { page },
  data() {
    var validatePass = (rule, value, callback) => {
      var reg = /^\d+$/
      if (!value) {
        callback(new Error('请输入工艺编号'))
      } else if (value && !reg.test(value)) {
        callback(new Error('工艺编号必须为纯数字'))
      } else {
        callback()
      }
    }
    var validatePass1 = (rule, value, callback) => {
      var reg = /^\d+$/
      if (!value) {
        callback(new Error('请输入工艺段ID'))
      } else if (value && !reg.test(value)) {
        callback(new Error('工艺段ID必须为纯数字'))
      } else {
        callback()
      }
    }
    return {
      tableData: [],
      total: 0,
      getParams: {},
      workshop_no: null,
      currentObj: { upper_rail_type: null, lower_rail_type: null },
      dialogVisible: false,
      rules: {
        process_code: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        process_ID: [
          { required: true, validator: validatePass1, trigger: 'blur' }
        ],
        process_name: [
          { required: true, message: '请填写工艺段名称', trigger: 'blur' }
        ],
        ordering: [
          { required: true, message: '请填写工艺段顺序', trigger: 'blur' }
        ],
        // workshop_no: [
        //   { required: true, message: '请填写车间号', trigger: 'blur' }
        // ],
        working_area: [
          { required: true, message: '请填写工作区', trigger: 'change' }
        ],
        cell_numbers: [
          { required: true, message: '请填写单车电池片数量', trigger: 'blur' }
        ],
        single_slot_num: [
          { required: true, message: '请填写单轴花篮数量', trigger: 'blur' }
        ],
        q_time: [
          { required: true, message: '请填写物料超时时间', trigger: 'blur' }
        ],
        warning_time: [
          { required: true, message: '请填写QTime预警时间', trigger: 'blur' }
        ],
        pitch_time: [
          { required: true, message: '请填写节拍', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      exportLoading: false,
      railType_list: [{ id: 1, name: '上料' }, { id: 2, name: '下料' }],
      basketType_list: [
        { id: 1, name: '空叠片盒' }, { id: 2, name: '满叠片盒' },
        { id: 3, name: '空湿花篮' }, { id: 4, name: '满湿花篮' },
        { id: 5, name: '空干花篮' }, { id: 6, name: '满干花篮' }
      ],
      process_list: [],
      area_list: [],
      dialogVisible1: false,
      cyclicGraphList: []
    }
  },
  created() {
    this.getList()
    // this.getWorkShop()
  },
  methods: {
    changeDebounce() {
      debounce(this, 'changeList')
    },
    async getList() {
      try {
        this.loading = true
        const data = await processSections('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getProcessList() {
      try {
        const data = await processSections('get', null, { params: { all: 1 } })
        this.process_list = data
      } catch (e) {
        //
      }
    },
    async getOtherList(val) {
      if (val) {
        try {
          const a = await Promise.all([
            workAreas('get', null, { params: { all: 1 } })
          ])
          this.area_list = a[0] || []
        } catch (e) {
          //
        }
      }
    },
    // async getWorkShop() {
    //   const data = await globalSettings('get', null, { })
    //   this.workshop_no = data.find(d => d.desc === '车间号')?.value
    // },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.getOtherList(true)
      // this.currentObj.workshop_no = this.workshop_no
      this.dialogVisible = true
    },
    editShow(row) {
      this.getOtherList(true)
      this.getProcessList()
      this.currentObj = Object.assign({}, row)
      // this.currentObj.workshop_no = this.workshop_no
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
      this.currentObj = { upper_rail_type: null, lower_rail_type: null }
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    writeId() {
      // if (this.currentObj.upper_rail_type === '') {
      //   this.$set(this.currentObj, 'upper_basket_type', null)
      // }
      // if (this.currentObj.lower_rail_type === '') {
      //   this.$set(this.currentObj, 'lower_basket_type', null)
      // }
      // if (!this.currentObj.upper_rail_type && !this.currentObj.lower_rail_type) {
      //   return
      // }
      // if (!this.currentObj.process_code || !this.currentObj.ordering) {
      //   this.$message.info('请先填写工艺编号和工艺序号')
      //   this.currentObj.upper_rail_type = null
      //   this.currentObj.lower_rail_type = null
      //   return
      // }
      // const d = outputString(this.currentObj.upper_rail_type, this.currentObj.lower_rail_type)
      // this.currentObj.process_ID = this.currentObj.ordering + this.currentObj.process_code + d
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
        processSectionsDel('post', null, { data: { obj_ids: arr } })
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
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            if (!this.currentObj.upper_rail_type && !this.currentObj.lower_rail_type) {
              this.$message.info('上层轨道上下料类型,下层轨道上下料类型至少选一个')
              return
            }
            if (this.currentObj.upper_rail_type && !this.currentObj.upper_basket_type) {
              this.$message.info('上层轨道上下料类型选择时上层花篮类型必填')
              return
            }
            if (this.currentObj.lower_rail_type && !this.currentObj.lower_basket_type) {
              this.$message.info('下层轨道上下料类型选择时下层花篮类型必填')
              return
            }
            if (this.currentObj.upper_rail_type === '') {
              this.currentObj.upper_rail_type = null
            }
            if (this.currentObj.upper_basket_type === '') {
              this.currentObj.upper_basket_type = null
            }
            if (this.currentObj.lower_rail_type === '') {
              this.currentObj.lower_rail_type = null
            }
            if (this.currentObj.lower_basket_type === '') {
              this.currentObj.lower_basket_type = null
            }
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await processSections(_api, this.currentObj.id || null, { data: this.currentObj })
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
    Upload(param) {
      const formData = new FormData()
      formData.append('file', param.file)
      this.$store.dispatch('settings/operateTypeSetting', '导入')
      processSectionsImport('post', null, { data: formData }).then(response => {
        this.$message({
          type: 'success',
          message: response
        })
        this.changeList()
      })
    },
    exportFun() {
      this.exportLoading = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = processSections
      this.$store.dispatch('settings/operateTypeSetting', '导出')
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.exportLoading = false
        }).catch(e => {
          this.exportLoading = false
        })
    },
    async arraySpanMethod(val) {
      try {
        const obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams, obj)
        const data = await processSections('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    },
    async showDialog() {
      this.dialogVisible1 = true
      try {
        const data = await processCyclicGraph('get', null, { params: {} })
        this.cyclicGraphList = data || []

        const option = {
          title: {
            text: ''
          },
          color: ['#5470c6'],
          tooltip: {},
          animationDurationUpdate: 1500,
          animationEasingUpdate: 'quinticInOut',
          series: [
            {
              type: 'graph',
              layout: 'none',
              symbolSize: 70,
              roam: true,
              label: {
                show: true
              },
              edgeSymbol: ['circle', 'arrow'],
              edgeSymbolSize: [4, 10],
              edgeLabel: {
                fontSize: 20
              },
              data: [],
              links: [],
              lineStyle: {
                opacity: 0.9,
                width: 2,
                curveness: 0
              }
            }
          ]
        }
        setTimeout(dd => {
          this.cyclicGraphList.forEach((d, i) => {
            const chartBar = echarts.init(document.getElementById('taskLine' + i))
            const obj = JSON.parse(JSON.stringify(option))
            obj.title.text = d.work_area
            obj.series[0].data = d.data
            obj.series[0].links = d.links
            chartBar.setOption(obj)
          })
        }, 300)
      } catch (e) {
        //
      }
    }
  }
}
function outputString(a, b) {
  if ((a === 1 && b !== 2) || (a !== 2 && b === 1)) {
    return '1'
  } else if ((a === 1 && b === 2) || (a === 2 && b === 1)) {
    return '3'
  } else if ((a === 2 && b !== 1) || (a !== 1 && b === 2)) {
    return '2'
  }
}
</script>

<style lang="scss">
.process_setting{
  .dialog-style{
  .el-input__inner{
  width: 200px;
}}
  .volumeBox{
    margin-bottom:20px;
    border:1px solid #eee;
  }
}
</style>

