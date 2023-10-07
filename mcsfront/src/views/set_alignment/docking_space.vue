<template>
  <div class="docking_space">
    <!-- 缓存停靠位配置 -->
    <div
      v-loading="loading"
      class="center-box"
    >
      <div class="botton-box">
        <el-button
          v-permission="['cache_device_conf','add']"
          type="blue"
          icon="el-icon-plus"
          size="small"
          @click="addFun"
        >新增</el-button>
        <el-button v-permission="['cache_device_conf','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['cache_device_conf','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button
          v-permission="['cache_device_conf','delete']"
          type="danger"
          icon="el-icon-delete"
          size="small"
          @click="deleteFun"
        >删除</el-button>
      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
        @selection-change="handleSelectionChange"
        @sort-change="arraySpanMethod"
      >
        <el-table-column
          type="selection"
          width="40"
        />
        <el-table-column label="停靠位ID" prop="location_ID" sortable="custom">
          <el-table-column
            min-width="20"
          >
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.location_ID" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.location_ID }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="停靠位名称" prop="location_name" sortable="custom">
          <el-table-column
            min-width="20"
          >
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.location_name" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.location_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="停靠位描述" prop="desc" sortable="custom">
          <el-table-column
            min-width="20"
          >
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.desc" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="停靠位描述" prop="workshop_no" sortable="custom">
          <el-table-column
            min-width="13"
          >
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.workshop_no" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.workshop_no }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="工作区" prop="working_area_name" sortable="custom">
          <el-table-column
            min-width="13"
          >
            <template slot="header" slot-scope="scope">
              <el-select
                v-model="getParams.working_area"
                size="small"
                placeholder=""
                clearable
                @change="changeList"
                @visible-change="getOtherList"
              >
                <el-option
                  v-for="item in area_list"
                  :key="item.id"
                  :label="item.area_name"
                  :value="item.id"
                />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.working_area_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="定线" prop="route_str" sortable="custom">
          <el-table-column
            min-width="13"
          >
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.route_str" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="{row}">
              {{ row.route_str }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="所属工艺段" prop="select_process_name" sortable="custom">
          <el-table-column
            min-width="13"
          >
            <template slot="header" slot-scope="scope">
              <el-select
                v-model="getParams.processes"
                size="small"
                placeholder=""
                clearable
                @change="changeList"
                @visible-change="getOtherList"
              >
                <el-option
                  v-for="item in process_list"
                  :key="item.id"
                  :label="item.process_name"
                  :value="item.id"
                />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.select_process_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建人" prop="created_username">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.created_username" size="small" clearable @input="changeDebounce" />
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_username?scope.row.created_username:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="创建时间" prop="created_time" sortable="custom">
          <el-table-column min-width="15">
            <template slot="header" slot-scope="scope">
              <el-date-picker
                value-format="yyyy-MM-dd"
                v-model="getParams.created_time"
                type="date"
                @change="changeList"
                placeholder="">
              </el-date-picker>
            </template>
            <template slot-scope="scope">
              {{ scope.row.created_time?scope.row.created_time:'--' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="启用标志" prop="is_used" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select
                v-model="getParams.is_used"
                clearable
                placeholder=""
                @change="changeList"
              >
                <el-option
                  v-for="item in [{name:'是',id:1},{name:'否',id:0}]"
                  :key="item.name"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </template>
            <template slot-scope="scope">
              <el-tag
                size="mini"
                style="border-radius: 20px"
                effect="dark"
                :type="scope.row.is_used?'success':'info'"
              >{{ scope.row.is_used?'是':'否' }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column
          label="操作"
          width="100"
        >
          <template slot-scope="{row}">
            <el-button
              v-permission="['cache_device_conf','change']"
              size="small"
              type="text"
              @click="editShow(row)"
            >修改</el-button>
            <el-button type="text" size="small" @click="editShow(row,true)">复制新增</el-button>
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
      :title="currentObj.id?'编辑':copyTrue?'复制-新增':'新建'"
      :visible.sync="dialogVisible"
      width="800px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form
        ref="ruleForm"
        inline
        :model="currentObj"
        :rules="rules"
        label-width="150px"
      >
        <el-form-item
          label="停靠位ID"
          prop="location_ID"
        >
          <el-input
            v-model="currentObj.location_ID"
            disabled
            size="small"
          />
        </el-form-item>
        <el-form-item
          label="停靠位编号"
          prop="location_code"
        >
          <el-input
            v-model="currentObj.location_code"
            size="small"
            @input="writeId(false)"
          />
        </el-form-item>
        <el-form-item
          label="停靠位名称"
          prop="location_name"
        >
          <el-input
            v-model="currentObj.location_name"
            size="small"
          />
        </el-form-item>
        <el-form-item
          label="停靠位描述"
          prop="desc"
        >
          <el-input
            v-model="currentObj.desc"
            size="small"
          />
        </el-form-item>
        <el-form-item
          label="工作区"
          prop="working_area"
        >
          <el-select
            v-model="currentObj.working_area"
            size="small"
            placeholder="请选择"
            @change="writeId(true)"
          >
            <el-option
              v-for="item in area_list"
              :key="item.id"
              :label="item.area_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="所属工艺段"
          prop="select_process"
        >
          <el-select
            v-model="currentObj.select_process"
            multiple
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
        </el-form-item>
        <el-form-item
          label="车间号"
          prop="workshop_no"
        >
          <el-input
            v-model="currentObj.workshop_no"
            disabled
            size="small"
          />
        </el-form-item>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button
          type="primary"
          :loading="btnLoading"
          @click="submitFun"
        >确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { debounce } from '@/utils'
import { restLocations, restLocationsDel, restLocationsUpdate, processSections } from '@/api/jqy'
import { workAreas, globalSettings } from '@/api/base_w'
import page from '@/components/page'
import common from '@/utils/common'
export default {
  name: 'DockingSpace',
  components: { page },
  data() {
    var validatePass = (rule, value, callback) => {
      var reg = /^\d+$/
      if (!value) {
        callback(new Error('请输入编号'))
      } else if (value && !reg.test(value)) {
        callback(new Error('站台编号必须为纯数字'))
      } else {
        callback()
      }
    }
    return {
      tableData: [],
      total: 0,
      getParams: {},
      workshop_no: null,
      currentObj: {
        select_process: []
      },
      dialogVisible: false,
      rules: {
        location_ID: [
          { required: true, message: '请填写停靠位ID', trigger: 'blur' }
        ],
        location_code: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        workshop_no: [
          { required: true, message: '请填写车间号', trigger: 'blur' }
        ],
        location_name: [
          { required: true, message: '请填写停靠位名称', trigger: 'blur' }
        ],
        select_process: [
          { required: true, message: '请填写所在工艺段', trigger: 'change' }
        ],
        working_area: [
          { required: true, message: '请填写工作区', trigger: 'change' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      process_list: [],
      workshop_list: [],
      area_list: [],
      copyTrue: false
    }
  },
  created() {
    this.getList()
    this.getWorkShop()
  },
  methods: {
    changeDebounce() {
      debounce(this, 'changeList')
    },
    async getList() {
      try {
        this.loading = true
        const data = await restLocations('get', null, { params: this.getParams })
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
        restLocationsUpdate('post', null, { data: { 'obj_ids': arr }})
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
    async getWorkShop() {
      const data = await globalSettings('get', null, { })
      this.workshop_no = data.find(d => d.desc === '车间号')?.value
    },
    async writeId(val) {
      if (!this.currentObj.working_area) {
        return
      }
      if (!this.currentObj.location_code) {
        this.$message('请先填写停靠位编号')
        this.currentObj.working_area = null
        return
      }
      const obj = this.area_list.find(d => d.id === this.currentObj.working_area)
      this.currentObj.location_ID = '3' + (obj ? obj.area_ID : '--') + this.currentObj.location_code
      if (val) {
        this.currentObj.select_process = []
      }
      const data = await processSections('get', null, { params: { all: 1, working_area: this.currentObj.working_area }})
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
    async getOtherList(val) {
      if (val) {
        try {
          const a = await Promise.all([
            workAreas('get', null, { params: { all: 1 }}),
            processSections('get', null, { params: { all: 1 }})
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
    addFun() {
      this.getOtherList(true)
      this.currentObj.workshop_no = this.workshop_no
      this.dialogVisible = true
    },
    editShow(row, bool) {
      // bool true是复制
      this.getOtherList(true)
      this.currentObj = Object.assign({}, row)
      this.currentObj.workshop_no = this.workshop_no
      if (bool) {
        delete this.currentObj.id
        this.currentObj.location_name = ''
        // this.currentObj.location_code = ''
        // this.currentObj.working_area = ''
      }
      this.dialogVisible = true
      this.copyTrue = bool
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    changeList() {
      if (this.getParams.processes === '') {
        delete this.getParams.processes
      }
      this.getParams.page = 1
      this.getList()
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {
        select_process: []
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
        restLocationsDel('post', null, { data: { obj_ids: arr }})
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
            await restLocations(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.getList()
            this.btnLoading = false
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            this.handleClose(null)
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    async arraySpanMethod(val) {
      try {
        let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams,obj)
        const data = await restLocations('get', null, { params: this.getParams})
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    }
  }
}
</script>

<style lang="scss">
.docking_space{
  .dialog-style{
  .el-input__inner{
  width: 200px;
}}}
</style>

