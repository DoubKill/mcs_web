<template>
  <div class="process_station_setting">
    <!-- 工艺站台配置 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['stations','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['stations','add']" type="blue" size="small" icon="el-icon-plus" @click="editShow(selection,true,true)">复制新增</el-button>
        <el-button v-permission="['stations','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['stations','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['stations','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <el-button v-permission="['stations','export']" type="blue" icon="el-icon-download" size="small" :loading="btnExportLoad" @click="templateDownload">导出</el-button>
        <el-button v-permission="['stations','export']" :loading="btnExportLoad1" type="blue" icon="el-icon-download" size="small" @click="downloadMould">
          导出Excel模板
        </el-button>
        <el-upload v-permission="['stations','import']" style="margin-left:8px;display:inline-block" action="string" accept=".xls, .xlsx" :http-request="Upload" :show-file-list="false">
          <el-button type="danger" :loading="btnExportLoad2" size="small">导入Excel</el-button>
        </el-upload>
      </div>
      <el-table ref="multipleTable" :data="tableData" tooltip-effect="dark" style="width: 100%" highlight-current-row stripe @selection-change="handleSelectionChange" @current-change="handleSelectionChange1" @sort-change="arraySpanMethod">
        <el-table-column type="selection" width="40" />
        <el-table-column label="站台ID" prop="platform_ID" sortable="custom">
          <el-table-column min-width="16">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.platform_ID" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.platform_ID }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="站台名称" prop="platform_name" sortable="custom">
          <el-table-column min-width="18">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.platform_name" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.platform_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="站台描述" prop="desc" sortable="custom">
          <el-table-column min-width="18">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.desc" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="位置点名称" prop="location_name" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.location_name" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.location_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="工作区" prop="working_area_name" sortable="custom">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.working_area" size="small" placeholder="" clearable @change="changeWorking" @visible-change="getOtherList">
                <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.working_area_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="所属工艺段" prop="process" sortable="custom">
          <el-table-column min-width="18">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.process" size="small" placeholder="" clearable @change="changeList" @visible-change="getOtherList">
                <el-option v-for="item in process_list" :key="item.id" :label="item.process_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.process_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column label="工艺段编号" prop="process_code" sortable="custom">
          <el-table-column min-width="20">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.process_code" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.process_code }}
            </template>
          </el-table-column>
        </el-table-column> -->
        <el-table-column label="上层轨道上下料类型" prop="upper_rail_type_name" sortable="custom">
          <el-table-column min-width="22">
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
        <el-table-column label="下层轨道上下料类型" prop="lower_rail_type_name" sortable="custom">
          <el-table-column min-width="22">
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
        <el-table-column label="物料超时时间(秒)" prop="q_time" sortable="custom">
          <el-table-column min-width="22">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.q_time" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.q_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="节拍(秒)" prop="pitch_time" sortable="custom">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.pitch_time" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.pitch_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建人" prop="created_username">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.created_username" prefix-icon="el-icon-search" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_username?scope.row.created_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_time" sortable="custom">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-date-picker v-model="getParams.created_time" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_time?scope.row.created_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="启用标志" prop="is_used" sortable="custom">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.is_used" size="small" clearable placeholder="" @change="changeList">
                <el-option v-for="item in [{name:'是',id:1},{name:'否',id:0}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'是':'否' }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <!-- <el-button
              v-permission="['cache_device_conf','change']"
              size="small"
              type="text"
              @click="editShow(row,true,false)"
            >配置属性</el-button> -->
            <el-button v-permission="['stations','change']" size="small" type="text" @click="editShow(row,false,false)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-footer id="footer">
      <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
    </el-footer>

    <el-dialog :title="copy?'复制新增':type?'属性配置':currentObj.id?'编辑':'新建'" :visible.sync="dialogVisible" width="860px" :before-close="handleClose" class="dialog-style">
      <el-form ref="ruleForm" inline :model="currentObj" :rules="rules" label-width="180px">
        <div v-if="!type||copy">
          <el-form-item label="站台ID" prop="platform_ID">
            <el-input v-model="currentObj.platform_ID" :disabled="currentObj.id?true:false" size="small" />
          </el-form-item>
          <el-form-item label="站台名称" prop="platform_name">
            <el-input v-model="currentObj.platform_name" :disabled="currentObj.id?true:false" size="small" />
          </el-form-item>
          <!-- <el-form-item
            label="站台编号"
            prop="platform_code"
          >
            <el-input
              v-model="currentObj.platform_code"
              :disabled="currentObj.id?true:false"
              size="small"
              @input="writeId(false)"
            />
          </el-form-item> -->
          <el-form-item label="站台描述" prop="desc">
            <el-input v-model="currentObj.desc" size="small" />
          </el-form-item>
          <el-form-item label="所属工艺段" prop="process">
            <el-select v-model="currentObj.process" style="width:184px" size="small" placeholder="请选择" @change="writeId(true)">
              <el-option v-for="item in process_list" :key="item.id" :label="item.process_name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="上层轨道上下料类型">
            <el-select v-model="currentObj.upper_rail_type" style="width:184px" size="small" disabled placeholder="">
              <el-option v-for="item in railType_list" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="上层花篮类型" prop="upper_basket_type">
            <el-select v-model="currentObj.upper_basket_type" style="width:184px" disabled size="small" placeholder="">
              <el-option v-for="item in basketType_list" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="下层轨道上下料类型" prop="lower_rail_type">
            <el-select v-model="currentObj.lower_rail_type" style="width:184px" disabled size="small" placeholder="">
              <el-option v-for="item in railType_list" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="下层花篮类型" prop="lower_basket_type">
            <el-select v-model="currentObj.lower_basket_type" style="width:184px" disabled size="small" placeholder="">
              <el-option v-for="item in basketType_list" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="物料超时时间(秒)" prop="q_time">
            <el-input-number v-model="currentObj.q_time" style="width:184px" size="small" controls-position="right" :min="0" />
          </el-form-item>
          <el-form-item label="节拍(秒)" prop="pitch_time">
            <el-input-number v-model="currentObj.pitch_time" style="width:184px" :step="1" step-strictly size="small" controls-position="right" :min="1" />
          </el-form-item>
          <el-form-item style="" label="位置点名称" prop="location_name">
            <el-input v-model="currentObj.location_name" size="small" @blur="changeText" />
          </el-form-item>
        </div>
        <!-- <el-form-item
          v-if="type&&!copy"
          label-width="80px"
          style=""
          label="站台名称"
          prop="location_name"
        >
          <el-input
            v-model="currentObj.platform_name"
            disabled
            size="small"
          />
        </el-form-item> -->
        <el-tabs v-if="!type||copy" v-model="activeName" v-loading="loadingDia">
          <el-tab-pane label="动作属性" name="first">
            <br>

            <el-row :gutter="20">
              <el-col v-for="(item,index) in currentObj.platform_parts" :key="index" :span="12">
                <el-form-item style="margin-left:-20px" :label="((index===0||index===1)?'上层':'下层')+((index===0||index===2)?'左侧辊道':'右侧辊道')" />
                <el-form-item style="" label="location">
                  <el-input v-model="item.location_ID" disabled size="small" />
                </el-form-item>
                <el-form-item style="" label="AGV动作">
                  <el-select v-model="item.part_type" size="small" style="width:184px" disabled placeholder="" clearable>
                    <el-option v-for="item1 in item.part_list" :key="item1.id" :label="item1.name" :value="item1.id" />
                  </el-select>
                </el-form-item>
                <el-form-item label="AGV轨道">
                  <el-select v-model="item.slot_no" disabled style="width:184px" size="small" placeholder="">
                    <el-option v-for="item1 in slot_list" :key="item1.id" :label="item1.name" :value="item1.name" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="料流转属性" name="second">
            <el-form-item label="所属定线">
              <el-input v-model="currentObj.route_name" size="small" disabled placeholder="" />
            </el-form-item>
            <br>
            <el-form-item label="物料来源(站台设备组)">
              <el-input v-model="currentObj.source_plt_group_name" size="small" disabled placeholder="" />
            </el-form-item>
            <el-form-item label="物料来源(堆栈设备组)">
              <el-input v-model="currentObj.source_cache_group_name" size="small" disabled placeholder="" />
            </el-form-item>
            <el-form-item label="物料去向(站台设备组)">
              <el-input v-model="currentObj.target_plt_group_name" size="small" disabled placeholder="" />
            </el-form-item>
            <el-form-item label="物料去向(堆栈设备组)">
              <el-input v-model="currentObj.target_cache_group_name" size="small" disabled placeholder="" />
            </el-form-item>
            <el-form-item label="分流来源设备组">
              <el-select v-model="currentObj.shunt_platform_group" multiple style="width:184px" clearable size="small" placeholder="" @visible-change="visibleChange">
                <el-option v-for="item in shunt_list" :key="item.id" :label="item.group_name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="分流阈值(车)" prop="shunt_threshold">
              <el-input v-model="currentObj.shunt_threshold" type="number" style="width:184px" size="small" />
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="任务属性" name="third">
            <el-form-item label="任务触发方式" prop="task_trigger_type">
              <el-select v-model="currentObj.task_trigger_type" size="small" :disabled="currentObj.platform_type !== 3" placeholder="任务触发方式">
                <el-option v-for="item in [{id:1,name:'以上料阈值'},{id:2,name:'以下料阈值'},{id:0,name:'上下互斥阈值'}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="休息位组" prop="location_group">
              <el-select v-model="currentObj.location_group" clearable size="small" placeholder="休息位组">
                <el-option v-for="item in location_group_list" :key="item.id" :label="item.group_name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="上料触发阈值(篮)">
              <el-input v-model="currentObj.up_task_trigger_threshold" :disabled="thresholdType===2" type="number" style="width:200px" size="small" :min="0" />
            </el-form-item>
            <el-form-item label="下料触发阈值(篮)">
              <el-input v-model="currentObj.down_task_trigger_threshold" :disabled="thresholdType===1" type="number" style="width:200px" size="small" :min="0" />
            </el-form-item>
            <el-form-item label="互斥站台">
              <el-select v-model="currentObj.rejected_platform" multiple clearable filterable size="small" placeholder="互斥站台">
                <el-option v-for="item in platform_list" :key="item.id" :label="item.platform_name" :value="item.id" />
              </el-select>
            </el-form-item>
            <!-- <el-form-item label="互斥站台阈值">
              <el-input v-model="currentObj.rejected_threshold" type="number" style="width:200px" size="small" :min="0" />
            </el-form-item> -->
            <el-form-item label="是否干式设备">
              <el-select v-model="currentObj.is_dry_type" clearable size="small" placeholder="是否干式设备" @change="changeWetGroup">
                <el-option v-for="item in [{id:true,name:'是'},{id:false,name:'否'}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="湿区设备限制组">
              <el-select v-model="currentObj.wet_limit_groups" :disabled="currentObj.is_dry_type===true" clearable size="small" placeholder="" multiple>
                <el-option v-for="item in out_list" :key="item.id" :label="item.group_name" :value="item.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="湿式设备组阈值">
              <el-input v-model="currentObj.wet_group_threshold" type="number" style="width:200px" size="small" :min="0" />
            </el-form-item>
            <el-form-item label="任务延迟时间(S)">
              <el-input v-model="currentObj.task_delay_time" type="number" style="width:200px" size="small" :min="0" />
            </el-form-item>
            <el-form-item label="优先级">
              <el-input v-model="currentObj.task_priority" type="number" style="width:200px" size="small" :min="0" />
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
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
import { platformGroup, workAreas } from '@/api/base_w'
import { platformInfoNew, platformInfoNewDel, platformInfoNewUpdate, processSections, locationGroups, downloadTemplate, platformInfoImport } from '@/api/jqy'
import common from '@/utils/common'
import page from '@/components/page'
export default {
  name: 'ProcessStationSetting',
  components: { page },
  data() {
    var validatePass = (rule, value, callback) => {
      var reg = /^\d+$/
      if (!value) {
        callback(new Error('请输入站台ID'))
      } else if (value && !reg.test(value)) {
        callback(new Error('站台ID必须为纯数字'))
      } else {
        callback()
      }
    }
    var validatePass1 = (rule, value, callback) => {
      if (value && value <= 0) {
        callback(new Error('必须大于0'))
      } else {
        callback()
      }
    }
    return {
      activeName: 'first',
      tableData: [],
      total: 0,
      out_list: [],
      getParams: {},
      currentObj: {
        up_task_trigger_threshold: undefined,
        down_task_trigger_threshold: undefined,
        task_trigger_type: null,
        shunt_platform_group: [],
        platform_parts: []
      },
      dialogVisible: false,
      rules: {
        platform_ID: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        platform_name: [
          { required: true, message: '请填写站台名称', trigger: 'blur' }
        ],
        desc: [
          { required: true, message: '请填写站台描述', trigger: 'change' }
        ],
        process: [
          { required: true, message: '请填写所在工艺段', trigger: 'change' }
        ],
        q_time: [
          { required: true, message: '请填写物料超时时间', trigger: 'blur' }
        ],
        pitch_time: [
          { required: true, message: '请填写节拍', trigger: 'blur' }
        ],
        location_name: [
          { required: true, message: '请填写位置点名称', trigger: 'blur' }
        ],
        task_trigger_type: [
          { required: true, message: '请填写任务触发方式', trigger: 'change' }
        ],
        shunt_threshold: [
          { required: false, validator: validatePass1, trigger: 'blur' }
        ]
      },
      currentVal: [],
      selection: {},
      thresholdType: 0,
      btnLoading: false,
      type: false,
      copy: false,
      loading: true,
      exportLoading: false,
      railType_list: [{ id: 1, name: '上料' }, { id: 2, name: '下料' }],
      basketType_list: [
        { id: 1, name: '空叠片盒' }, { id: 2, name: '满叠片盒' },
        { id: 3, name: '空湿花篮' }, { id: 4, name: '满湿花篮' },
        { id: 5, name: '空干花篮' }, { id: 6, name: '满干花篮' }
      ],
      slot_list: [
        { id: 1, name: 'G1A' }, { id: 2, name: 'G1B' },
        { id: 3, name: 'G2A' }, { id: 4, name: 'G2B' }
      ],
      part_list: [
        { id: 1, name: '取货' }, { id: 2, name: '卸货' }
      ],
      loadingDia: false,
      shunt_list: [],
      location_group_list: [],
      process_list: [],
      platform_list: [],
      area_list: [],
      working_area: null,
      btnExportLoad: false,
      btnExportLoad1: false,
      btnExportLoad2: false
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
        const data = await platformInfoNew('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    },
    changeWetGroup() {
      if (this.currentObj.is_dry_type) {
        this.$set(this.currentObj, 'wet_limit_groups', [])
      }
    },
    changeDebounce() {
      debounce(this, 'changeList')
    },
    async visibleChange(val) {
      if (val && this.currentObj.id) {
        const data = await platformGroup('get', null, { params: { all: 1, group_type: 1, process: this.currentObj.source_process } })
        this.shunt_list = data || []

        // 过滤掉本身线体
        let arr = this.shunt_list.filter(d => {
          return d.group_name !== this.currentObj.source_plt_group_name
        })
        this.shunt_list = arr
      }
    },
    changeText() {
      if (this.currentObj.location_name) {
        this.currentObj.platform_parts.forEach((d, index) => {
          d.location_ID = this.currentObj.location_name + '_' + (4 - index)
        })
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await platformInfoNew('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
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
        platformInfoNewUpdate('post', null, { data: { 'obj_ids': arr } })
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
    clearObject(obj) {
      for (var key in obj) {
        if (typeof obj[key] === 'object' && obj[key] !== null) {
          this.clearObject(obj[key]) // 递归清空嵌套的对象
        }
        if (obj[key] === '') {
          this.$set(obj, key, null)
        } // 使用Vue.set进行属性赋值，确保响应式更新
      }
    },
    async writeId(val) {
      if (!this.currentObj.process) {
        return
      }
      this.$set(this.currentObj, 'rejected_platform', undefined)
      let working_area = this.process_list.find(d => d.id === this.currentObj.process).working_area
      const data = await platformInfoNew('get', null, { params: { all: 1, working_area: working_area } })
      this.platform_list = data

      const b = this.process_list.find(d => d.id === this.currentObj.process).upper_rail_type
      const c = this.process_list.find(d => d.id === this.currentObj.process).lower_rail_type
      const d = outputString(b, c)
      this.thresholdType = Number(d)
      this.$set(this.currentObj, 'up_task_trigger_threshold', undefined)
      this.$set(this.currentObj, 'down_task_trigger_threshold', undefined)
      this.currentObj.platform_type = Number(d)
      if (val) {
        this.currentObj.q_time = this.process_list.find(d => d.id === this.currentObj.process).q_time
        this.currentObj.pitch_time = this.process_list.find(d => d.id === this.currentObj.process).pitch_time
        this.currentObj.upper_rail_type = this.process_list.find(d => d.id === this.currentObj.process).upper_rail_type
        this.currentObj.upper_basket_type = this.process_list.find(d => d.id === this.currentObj.process).upper_basket_type
        this.currentObj.lower_rail_type = this.process_list.find(d => d.id === this.currentObj.process).lower_rail_type
        this.currentObj.lower_basket_type = this.process_list.find(d => d.id === this.currentObj.process).lower_basket_type
        const parts1 = outputChange(this.currentObj.upper_rail_type)
        const parts2 = outputChange(this.currentObj.lower_rail_type)
        this.currentObj.platform_parts[0].part_list = this.part_list.filter(d => d.id === parts1)
        this.currentObj.platform_parts[0].part_type = parts1
        this.currentObj.platform_parts[1].part_list = this.part_list.filter(d => d.id === parts1)
        this.currentObj.platform_parts[1].part_type = parts1
        this.currentObj.platform_parts[2].part_list = this.part_list.filter(d => d.id === parts2)
        this.currentObj.platform_parts[2].part_type = parts2
        this.currentObj.platform_parts[3].part_list = this.part_list.filter(d => d.id === parts2)
        this.currentObj.platform_parts[3].part_type = parts2
        this.currentObj.task_trigger_type = (this.currentObj.platform_type === 3 ? null : this.currentObj.platform_type)
        const a = this.process_list.find(d => d.id === this.currentObj.process).source_process
        this.currentObj.shunt_platform_group = []
        if (a) {
          const data = await platformGroup('get', null, { params: { all: 1, group_type: 1, process: a } })
          this.shunt_list = data
        } else {
          this.shunt_list = []
        }
      }
    },
    changeWorking() {
      this.$set(this.getParams, 'process', null)
      this.process_list = []
      this.changeList()
    },
    async getOtherList(val) {
      if (val) {
        try {
          const a = await Promise.all([
            workAreas('get', null, { params: { all: 1 } }),
            processSections('get', null, { params: { all: 1, working_area: this.getParams.working_area } }),
            platformGroup('get', null, { params: { all: 1, group_type: 1, out_rail_flat: 1 } }),
            locationGroups('get', null, { params: { all: 1 } })
          ])
          this.area_list = a[0] || []
          this.process_list = a[1] || []
          this.out_list = a[2] || []
          this.location_group_list = a[3] || []
        } catch (e) {
          //
        }
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    handleSelectionChange1(val) {
      this.selection = val || []
    },
    async addFun() {
      this.type = false
      this.copy = false
      this.getOtherList(true)
      this.currentObj = {
        task_trigger_type: null,
        shunt_platform_group: [],
        platform_parts: []
      }
      this.currentObj.platform_parts = [{
        'slot_no': 'G2B',
        'location_ID': '',
        'part_type': null,
        'part_list': [],
        'axis_no': 1
      }, {
        'slot_no': 'G2A',
        'location_ID': '',
        'part_type': null,
        'part_list': [],
        'axis_no': 2
      }, {
        'slot_no': 'G1B',
        'location_ID': '',
        'part_type': null,
        'part_list': [],
        'axis_no': 3
      }, {
        'slot_no': 'G1A',
        'location_ID': '',
        'part_type': null,
        'part_list': [],
        'axis_no': 4
      }]
      this.activeName = 'first'
      this.$set(this.currentObj, 'task_priority', 5)
      this.dialogVisible = true
      const data = await platformInfoNew('get', null, { params: { all: 1 } })
      this.platform_list = data
    },
    async editShow(row, val, val1) {
      if (JSON.stringify(row) !== '{}') {
        this.type = val
        this.copy = val1
        this.dialogVisible = true
        const currentObj = JSON.parse(JSON.stringify(row))
        this.thresholdType = currentObj.platform_type
        this.loadingDia = true
        const data1 = await platformInfoNew('get', row.id, { params: {} })
        this.currentObj = Object.assign({}, data1)
        this.currentObj.platform_type = currentObj.platform_type
        this.activeName = 'first'
        const data = await platformInfoNew('get', null, { params: { all: 1, working_area: this.currentObj.working_area } })
        this.platform_list = data
        const parts1 = outputChange(this.currentObj.upper_rail_type)
        const parts2 = outputChange(this.currentObj.lower_rail_type)
        if (this.currentObj.platform_parts.length === 0) {
          this.currentObj.platform_parts = [{
            'slot_no': 'G2B',
            'location_ID': '',
            'platform_info_id': this.currentObj.id,
            'axis_no': 1,
            'part_list': this.part_list.filter(d => d.id === parts1),
            'part_type': this.currentObj.upper_rail_type,
            'is_used': this.currentObj.upper_rail_type !== null
          }, {
            'slot_no': 'G2A',
            'location_ID': '',
            'platform_info_id': this.currentObj.id,
            'axis_no': 2,
            'part_list': this.part_list.filter(d => d.id === parts1),
            'part_type': this.currentObj.upper_rail_type,
            'is_used': this.currentObj.upper_rail_type !== null
          }, {
            'slot_no': 'G1B',
            'location_ID': '',
            'platform_info_id': this.currentObj.id,
            'axis_no': 3,
            'part_list': this.part_list.filter(d => d.id === parts2),
            'part_type': this.currentObj.lower_rail_type,
            'is_used': this.currentObj.lower_rail_type !== null
          }, {
            'slot_no': 'G1A',
            'location_ID': '',
            'platform_info_id': this.currentObj.id,
            'axis_no': 4,
            'part_list': this.part_list.filter(d => d.id === parts2),
            'part_type': this.currentObj.lower_rail_type,
            'is_used': this.currentObj.lower_rail_type !== null
          }]
          this.$set(this.currentObj, 'task_priority', 5)
          this.currentObj.task_trigger_type = (currentObj.platform_type === 3 ? null : currentObj.platform_type)
        } else {
          this.currentObj.platform_parts.forEach((item, index) => {
            if (index <= 1) {
              item.part_list = this.part_list.filter(d => d.id === parts1)
            } else {
              item.part_list = this.part_list.filter(d => d.id === parts2)
            }
          })
        }
        this.loadingDia = false
        this.getOtherList(true)
        this.visibleChange(true)
        if (val1) {
          delete this.currentObj.id
          this.currentObj.platform_ID = null
          this.currentObj.platform_code = null
          this.currentObj.platform_name = null
          this.currentObj.desc = null
          this.currentObj.location_name = null
          this.currentObj.platform_parts.forEach(d => { d.location_ID = '' })
        }
      } else {
        this.loadingDia = true
        this.$message('请选中一行数据')
      }
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
      this.currentObj = {
        platform_parts: []
      }
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
        platformInfoNewDel('post', null, { data: { obj_ids: arr } })
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
      if (this.thresholdType === 1 && isEmpty(this.currentObj.up_task_trigger_threshold)) {
        this.$message.info('上料触发阈值必填')
        return
      } else if (this.thresholdType === 2 && isEmpty(this.currentObj.down_task_trigger_threshold)) {
        this.$message.info('下料触发阈值必填')
        return
      } else if (this.thresholdType === 3 && (isEmpty(this.currentObj.up_task_trigger_threshold) || isEmpty(this.currentObj.down_task_trigger_threshold))) {
        this.$message.info('上下料触发阈值必填')
        return
      }
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            this.clearObject(this.currentObj)
            this.btnLoading = true
            this.currentObj.other_change = this.type
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await platformInfoNew(_api, this.currentObj.id || null, { data: this.currentObj })
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
    templateDownload() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = platformInfoNew
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    },
    downloadMould() {
      this.btnExportLoad1 = true
      downloadTemplate({}).then(response => {
        const link = document.createElement('a')
        const blob = new Blob([response], { type: 'application/vnd.ms-excel' })
        link.style.display = 'none'
        link.href = URL.createObjectURL(blob)
        link.download = '工艺站台列表模板.xlsx'// 下载的文件名
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        this.btnExportLoad1 = false
      }).catch(e => {
        this.btnExportLoad1 = false
      })
    },
    Upload(param) {
      this.btnExportLoad2 = true
      const formData = new FormData()
      formData.append('file', param.file)
      platformInfoImport('post', null, { data: formData }).then(response => {
        this.$store.dispatch('settings/operateTypeSetting', '导入')
        this.btnExportLoad2 = false
        this.$message({
          type: 'success',
          message: response
        })
        this.changeList()
      }).catch(e => {
        this.btnExportLoad2 = false
      })
    },
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
function outputChange(a) {
  if (a === 1) {
    return 2
  } else if (a === 2) {
    return 1
  } else {
    return null
  }
}
function isEmpty(value) {
  return value === undefined || value === null || value === ''
}
</script>

<style lang="scss">
</style>

