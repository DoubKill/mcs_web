<template>
  <div class="exit_platform_setting">
    <!-- 堆栈站台配置 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['caches','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['caches','add']" type="blue" size="small" icon="el-icon-plus" @click="editShow(selection,true)">复制新增</el-button>
        <!-- v-permission="['caches','update']" -->
        <el-button type="danger" icon="el-icon-turn-off" size="small" @click="useFun('进料禁用',1)">进料禁用</el-button>
        <el-button type="danger" icon="el-icon-open" size="small" @click="useFun('进料启用',1)">进料启用</el-button>
        <el-button type="blue" icon="el-icon-turn-off" size="small" @click="useFun('出料禁用',2)">出料禁用</el-button>
        <el-button type="blue" icon="el-icon-open" size="small" @click="useFun('出料启用',2)">出料启用</el-button>
        <el-button v-permission="['caches','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <!-- <el-switch v-model="aaa" style="margin:0 10px" @change="useFun($event,1)" active-text="进料启用" inactive-text="进料禁用">
        </el-switch>
        <el-switch v-model="bbb" style="margin:0 10px" @change="useFun($event,2)" active-text="出料启用" inactive-text="出料禁用">
        </el-switch> -->
      </div>
      <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" style="width: 100%" highlight-current-row stripe row-key="id" @selection-change="handleSelectionChange" @current-change="handleSelectionChange1" @sort-change="arraySpanMethod">
        <el-table-column type="selection" width="40" />
        <el-table-column label="站台ID" prop="device_ID" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.device_ID" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.device_ID }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="站台名称" prop="device_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.device_name" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.device_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column label="站台编号" prop="device_code" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.device_code" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.device_code }}
            </template>
          </el-table-column>
        </el-table-column> -->
        <el-table-column label="站台描述" prop="desc" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.desc" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="进料位置点" prop="in_location_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.in_location_name" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.in_location_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="出料位置点" prop="out_location_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.out_location_name" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.out_location_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column label="车间号" prop="workshop_no" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.workshop_no" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.workshop_no }}
            </template>
          </el-table-column>
        </el-table-column> -->
        <el-table-column label="所属定线" prop="route_schemas" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.route_schemas" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.route_schemas.join(',') }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="工作区" prop="working_area_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.working_area" size="small" placeholder="请选择" clearable @change="changeList" @visible-change="getOtherList($event,true)">
                <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.working_area_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="所属工艺段">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.process" size="small" placeholder="请选择" clearable @change="changeList" @visible-change="getOtherList($event,true)">
                <el-option v-for="item in process_list" :key="item.id" :label="item.process_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.processes.join() }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column
          prop="task_delay_time"
          label="任务延迟时间(S)"
          min-width="20"
        /> -->
        <el-table-column label="允许任务数" prop="allow_task_num" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.allow_task_num" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.allow_task_num }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="任务优先级" prop="task_priority" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.task_priority" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.task_priority }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column
          prop="created_time"
          label="创建时间"
          min-width="20"
          sortable="custom"
        />
        <el-table-column
          prop="created_username"
          label="创建人"
          min-width="20"
          sortable="custom"
        /> -->
        <el-table-column label="进料启用" prop="in_is_used">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.in_is_used" size="small" clearable placeholder="" @change="changeList">
                <el-option v-for="item in [{name:'是',id:true},{name:'否',id:false}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.in_is_used?'success':'info'">{{ scope.row.in_is_used?'是':'否' }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="出料启用" prop="out_is_used">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.out_is_used" size="small" clearable placeholder="" @change="changeList">
                <el-option v-for="item in [{name:'是',id:true},{name:'否',id:false}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.out_is_used?'success':'info'">{{ scope.row.out_is_used?'是':'否' }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template slot-scope="{row}">
            <el-button v-permission="['caches','change']" size="small" type="text" @click="editShow(row,false)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>
    <el-dialog :title="copy?'复制新增':currentObj.id?'编辑':'新建'" :visible.sync="dialogVisible" width="900px" :before-close="handleClose" class="dialog-style">
      <el-form ref="ruleForm" v-loading="loadingDia" inline :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="站台ID" prop="device_ID">
          <el-input v-model="currentObj.device_ID" :disabled="!copy&&currentObj.id?true:false" size="small" />
        </el-form-item>
        <el-form-item label="站台名称" prop="device_name">
          <el-input v-model="currentObj.device_name" size="small" :disabled="!copy&&currentObj.id?true:false" />
        </el-form-item>
        <!-- <el-form-item label="站台编号" prop="device_code">
          <el-input v-model="currentObj.device_code" size="small" @input="writeId(false)" :disabled="!copy&&currentObj.id?true:false" />
        </el-form-item> -->
        <el-form-item label="站台描述" prop="desc">
          <el-input v-model="currentObj.desc" size="small" />
        </el-form-item>
        <!-- <el-form-item label="车间号" prop="workshop_no">
          <el-input v-model="currentObj.workshop_no" disabled size="small" />
        </el-form-item> -->
        <el-form-item label="工作区" prop="working_area">
          <el-select v-model="currentObj.working_area" size="small" placeholder="请选择" @change="changeWorking" @visible-change="getOtherList($event,false)">
            <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="任务延迟时间(S)" prop="task_delay_time">
          <el-input-number
            v-model="currentObj.task_delay_time"
            style="width:200px"
            size="small"
            controls-position="right"
            :min="0"
          />
        </el-form-item> -->
        <el-form-item label="允许任务数" prop="allow_task_num">
          <el-input-number v-model="currentObj.allow_task_num" style="width:200px" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="任务优先级" prop="task_priority">
          <el-input-number v-model="currentObj.task_priority" style="width:200px" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="所属工艺段" prop="processes">
          <el-select v-model="currentObj.processes" size="small" placeholder="请选择" clearable multiple @visible-change="getOtherList($event,false)">
            <el-option v-for="item in process_list" :key="item.id" :label="item.process_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="排" prop="row_num" class="row_num_style">
          <el-input-number v-model="currentObj.row_num" style="width:60px" size="small" controls-position="right" :min="1" :disabled="!copy&&currentObj.id?true:false" />
        </el-form-item>
        <div class="column_num_style">
          <el-form-item label="列" prop="column_num" class="row_num_style">
            <el-input-number v-model="currentObj.column_num" style="width:60px" size="small" controls-position="right" :min="1" :disabled="!copy&&currentObj.id?true:false" />
          </el-form-item>
          <el-form-item label="层" prop="layer_num" class="row_num_style">
            <el-input-number v-model="currentObj.layer_num" style="width:60px" size="small" controls-position="right" :min="1" :disabled="!copy&&currentObj.id?true:false" />
          </el-form-item>
        </div>
        <!-- <el-form-item
          label="所属工艺段"
          class="setProcessStyle"
        >
          <el-table
            style="width:650px;margin-left:150px;margin-top:-25px"
            :data="currentObj.device_process"
            tooltip-effect="dark"
            stripe
          >
            <el-table-column
              label="工艺段"
              min-width="30"
            >
              <template slot-scope="{row}">
                <el-select
                  v-model="row.process"
                  size="small"
                  placeholder="请选择"
                  clearable
                  @visible-change="visibleChange"
                >
                  <el-option
                    v-for="item in process_list"
                    :key="item.id"
                    :label="item.process_name"
                    :value="item.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column
              label="进料阈值"
              min-width="30"
            >
              <template slot-scope="{row}">
                <el-input-number v-model="row.in_task_threshold" controls-position="right" size="small" />
              </template>
            </el-table-column>
            <el-table-column
              label="出料阈值"
              min-width="30"
            >
              <template slot-scope="{row}">
                <el-input-number v-model="row.out_task_threshold" controls-position="right" size="small" />
              </template>
            </el-table-column>
            <el-table-column
              label="优先级"
              min-width="30"
            >
              <template slot-scope="{row}">
                <el-input-number v-model="row.task_priority" controls-position="right" size="small" />
              </template>
            </el-table-column>
            <el-table-column
              label="操作"
              min-width="20"
            >
              <template slot-scope="scope">
                <el-button type="danger" icon="el-icon-delete" size="small" @click="dialogDeleteFun(scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="text-align: center;margin-left:150px">
            <el-button type="primary" size="small" @click="addDialogFun">插入一行</el-button>
          </div>
        </el-form-item><br> -->
        <el-form-item label="进料口位置点名称" prop="in_location_name">
          <el-input v-model="currentObj.in_location_name" size="small" @blur="changeText" />
        </el-form-item>
        <el-form-item label="进料启用">
          <el-radio-group v-model="currentObj.in_is_used">
            <el-radio :label="true">启用</el-radio>
            <el-radio :label="false">屏蔽</el-radio>
          </el-radio-group>
        </el-form-item>
        <br>
        <el-row :gutter="20">
          <el-col v-for="(item,index) in currentObj.device_parts1" :key="index" :span="12">
            <el-form-item style="margin-left:-20px" :label="((index===0||index===1)?'上层':'下层')+((index===0||index===2)?'左侧辊道':'右侧辊道')" />
            <el-form-item style="" label="location">
              <el-input disabled v-model="item.location_ID" size="small" />
            </el-form-item>
            <el-form-item style="" label="AGV轨道">
              <el-select disabled v-model="item.slot_no" size="small" placeholder="">
                <el-option v-for="item1 in slot_list" :key="item1.id" :label="item1.name" :value="item1.name" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider />
        <el-form-item label="出料口位置点名称" prop="out_location_name">
          <el-input v-model="currentObj.out_location_name" size="small" @blur="changeText1" />
        </el-form-item>
        <el-form-item label="出料启用">
          <el-radio-group v-model="currentObj.out_is_used">
            <el-radio :label="true">启用</el-radio>
            <el-radio :label="false">屏蔽</el-radio>
          </el-radio-group>
        </el-form-item>
        <br>
        <el-row :gutter="20">
          <el-col v-for="(item,index) in currentObj.device_parts2" :key="index" :span="12">
            <el-form-item style="margin-left:-20px" :label="((index===0||index===1)?'上层':'下层')+((index===0||index===2)?'左侧辊道':'右侧辊道')" />
            <el-form-item style="" label="location">
              <el-input disabled v-model="item.location_ID" size="small" />
            </el-form-item>
            <el-form-item style="" label="AGV轨道">
              <el-select disabled v-model="item.slot_no" size="small" placeholder="">
                <el-option v-for="item1 in slot_list" :key="item1.id" :label="item1.name" :value="item1.name" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from '@/utils'
import { cacheDeviceInfo, cacheDeviceInfoDel, cacheDeviceInfoUpdate, processSections } from '@/api/jqy'
import { workAreas, globalSettings } from '@/api/base_w'
import common from '@/utils/common'
import page from '@/components/page'
export default {
  name: 'ExitPlatformSetting',
  components: { page },
  data() {
    var validatePass = (rule, value, callback) => {
      var reg = /^\d+$/
      if (!value) {
        callback(new Error('请输入站台编号'))
      } else if (value && !reg.test(value)) {
        callback(new Error('站台编号必须为纯数字'))
      } else {
        callback()
      }
    }
    var validatePass1 = (rule, value, callback) => {
      var reg = /^\d+$/
      if (!value) {
        callback(new Error('请输入站台ID'))
      } else if (value && !reg.test(value)) {
        callback(new Error('站台ID必须为纯数字'))
      } else {
        callback()
      }
    }
    return {
      tableData: [],
      total: 0,
      copy: false,
      getParams: {},
      selection: {},
      workshop_no: null,
      currentObj: {
        device_parts1: [],
        device_parts2: [],
        device_process: []
      },
      loadingDia: false,
      slot_list: [
        { id: 1, name: 'G1A' }, { id: 2, name: 'G1B' },
        { id: 3, name: 'G2A' }, { id: 4, name: 'G2B' }
      ],
      dialogVisible: false,
      rules: {
        device_code: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        device_ID: [
          { required: true, validator: validatePass1, trigger: 'blur' }
        ],
        device_name: [
          { required: true, message: '请填写站台名称', trigger: 'blur' }
        ],
        desc: [
          { required: true, message: '请填写站台描述', trigger: 'blur' }
        ],
        allow_task_num: [
          { required: true, message: '请填写允许任务数', trigger: 'blur' }
        ],
        processes: [
          { required: true, message: '请选择', trigger: 'blur' }
        ],
        row_num: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        column_num: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        layer_num: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        // workshop_no: [
        //   { required: true, message: '请填写车间号', trigger: 'blur' }
        // ],
        working_area: [
          { required: true, message: '请填写工作区', trigger: 'blur' }
        ],
        in_location_name: [
          { required: true, message: '请填写进料口位置点名称', trigger: 'blur' }
        ],
        out_location_name: [
          { required: true, message: '请填写出料口位置点名称', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      process_list: [],
      area_list: [],
      sideList: [],
      aaa: null,
      bbb: null
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async arraySpanMethod(val) {
      try {
        const obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams, obj)
        const data = await cacheDeviceInfo('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    },
    changeText() {
      if (this.currentObj.in_location_name) {
        this.currentObj.device_parts1.forEach((d, index) => {
          d.location_ID = this.currentObj.in_location_name + '_' + (4 - index)
        })
      }
    },
    changeText1() {
      if (this.currentObj.out_location_name) {
        this.currentObj.device_parts2.forEach((d, index) => {
          d.location_ID = this.currentObj.out_location_name + '_' + (4 - index)
        })
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await cacheDeviceInfo('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    changeDebounce() {
      debounce(this, 'changeList')
    },
    useFun(val, bool) {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      const arrName = []
      this.currentVal.forEach(d => {
        if (val.indexOf('禁用') > -1 && (bool === 1 ? d.in_is_used : d.out_is_used)) {
          arr.push(d.id)
          arrName.push(d.device_name)
        } else if (val.indexOf('启用') > -1 && (bool === 1 ? !d.in_is_used : !d.out_is_used)) {
          arr.push(d.id)
          arrName.push(d.device_name)
        }
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        cacheDeviceInfoUpdate('post', null, { data: { 'obj_ids': arr, operator_type: bool } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.changeList()
            this.$store.dispatch('settings/operateTypeSetting', val + arrName)
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    changeWorking() {
      this.$set(this.currentObj, 'processes', [])
      this.process_list = []
    },
    async writeId(val) {
      if (!this.currentObj.working_area) {
        return
      }
      // if (!this.currentObj.device_code) {
      //   this.$message('请先填写站台编号')
      //   this.currentObj.working_area = null
      //   return
      // }
      // this.currentObj.device_ID = '2' + (this.currentObj.working_area < 10 ? '0' + this.currentObj.working_area : this.currentObj.working_area) + this.currentObj.device_code
      this.$set(this.currentObj, 'processes', null)
      if (val) {
        this.currentObj.device_process = []
      }
      const data = await processSections('get', null, { params: { all: 1, working_area: this.currentObj.working_area, out_rail_flat: 1 } })
      this.process_list = data || []
    },
    visibleChange(val) {
      if (val) {
        if (!this.currentObj.working_area) {
          this.$message.info('请先选择工作区')
          this.process_list = []
          return
        }
      }
    },
    async getOtherList(val, bool) {
      if (val) {
        try {
          const a = await Promise.all([
            workAreas('get', null, { params: { all: 1 } }),
            processSections('get', null, { params: { all: 1, out_rail_flat: 1, working_area: bool ? this.getParams.working_area : this.currentObj.working_area } })
          ])
          this.area_list = a[0] || []
          this.process_list = a[1] || []
        } catch (e) {
          //
        }
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    handleSelectionChange1(val) {
      this.selection = val
    },
    async addFun() {
      this.copy = false
      // this.getOtherList(true)
      this.currentObj.workshop_no = this.workshop_no
      this.currentObj.device_parts1 = [{
        'slot_no': 'G2B',
        'location_ID': '',
        'axis_no': 1,
        'part_type': 2
      }, {
        'slot_no': 'G2A',
        'location_ID': '',
        'axis_no': 2,
        'part_type': 2
      }, {
        'slot_no': 'G1B',
        'location_ID': '',
        'axis_no': 3,
        'part_type': 2
      }, {
        'slot_no': 'G1A',
        'location_ID': '',
        'axis_no': 4,
        'part_type': 2
      }]
      this.currentObj.device_parts2 = [{
        'slot_no': 'G2B',
        'location_ID': '',
        'axis_no': 5,
        'part_type': 1
      }, {
        'slot_no': 'G2A',
        'location_ID': '',
        'axis_no': 6,
        'part_type': 1
      }, {
        'slot_no': 'G1B',
        'location_ID': '',
        'axis_no': 7,
        'part_type': 1
      }, {
        'slot_no': 'G1A',
        'location_ID': '',
        'axis_no': 8,
        'part_type': 1
      }]
      this.$set(this.currentObj, 'out_is_used', true)
      this.$set(this.currentObj, 'in_is_used', true)
      this.dialogVisible = true
    },
    // async getWorkShop() {
    //   const data = await globalSettings('get', null, {})
    //   this.workshop_no = data.find(d => d.desc === '车间号')?.value
    // },
    async editShow(row, val) {
      this.copy = val
      if (JSON.stringify(row) !== '{}') {
        this.currentObj.working_area = row.working_area
        this.getOtherList(true, false)
        this.dialogVisible = true
        this.loadingDia = true
        const data1 = await cacheDeviceInfo('get', row.id, { params: {} })
        this.currentObj.workshop_no = this.workshop_no
        this.currentObj = Object.assign({}, data1)
        this.currentObj.device_parts.sort((a, b) => a.axis_no - b.axis_no)
        this.currentObj.device_parts1 = this.currentObj.device_parts.slice(0, 4)
        this.currentObj.device_parts2 = this.currentObj.device_parts.slice(4, 8)
        if (val) {
          delete this.currentObj.id
          this.currentObj.device_ID = null
          this.currentObj.device_name = null
          this.currentObj.device_code = null
          this.currentObj.desc = null
          this.currentObj.in_location_name = null
          this.currentObj.out_location_name = null
          this.currentObj.device_parts1.forEach(d => { d.location_ID = '' })
          this.currentObj.device_parts2.forEach(d => { d.location_ID = '' })
        }
        this.loadingDia = false
      } else {
        this.$message('请选中一行数据')
      }
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    changeList() {
      if (this.getParams.process === '') {
        delete this.getParams.process
      }
      this.getParams.page = 1
      this.getList()
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {
        device_parts1: [],
        device_parts2: []
      }
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    addDialogFun() {
      if (!this.currentObj.device_process) {
        this.$set(this.currentObj, 'device_process', [])
      }
      this.currentObj.device_process.push({})
    },
    dialogDeleteFun(index) {
      this.currentObj.device_process.splice(index, 1)
    },
    deleteFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      const arrName = []
      this.currentVal.forEach(d => {
        arr.push(d.id)
        arrName.push(d.device_name)
      })
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        cacheDeviceInfoDel('post', null, { data: { obj_ids: arr } })
          .then((response) => {
            this.$store.dispatch('settings/operateTypeSetting', '删除' + arrName)
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
            this.currentObj.device_parts = this.currentObj.device_parts1.concat(this.currentObj.device_parts2)
            this.currentObj.device_parts.forEach(d => {
              if (!d.location_ID) {
                throw new Error('location必填')
              }
            })
            // if (this.currentObj.device_process.length === 0) {
            //   this.$message('所属工艺段必填')
            //   return
            // }
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            await cacheDeviceInfo(_api, this.currentObj.id || null, { data: this.currentObj })
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更'+ this.currentObj.device_name)
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增'+ this.currentObj.device_name)
            }
            this.$message.success('操作成功')
            this.handleClose(null)
            this.getList()
            this.btnLoading = false
          } catch (e) {
            this.btnLoading = false
            if (e.message) {
              this.$message(e.message)
            }
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
  .exit_platform_setting{
    .dialog-style{
    .el-input__inner{
    width: 200px;
  }
  .el-table .cell{
    text-overflow:clip;
  }
  .setProcessStyle{
    .el-form-item__content{
        width: 100%;
    }
    .el-input__inner{
    width: 130px;
  }
  // .el-input-number--small{
    // width: 130px;
  // }
  .el-input-number .el-input__inner{
    width: 130px;
  }
  }
}
  .column_num_style{
    width: 241px !important;
    display: inline-block;
    .el-form-item__label{
      width: 40px !important;
    }
  }
  .row_num_style{
      .el-input__inner{
        width: 100% !important;
        padding-right: 10px !important;
        padding-left: 10px !important;
      }
      .el-input-number__decrease,.el-input-number__increase{
        display: none;
      }
    }

}

  </style>

