<template>
  <div>
    <!-- AGV管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="AGV名称">
          <el-input v-model="getParams.rack_name" size="small" clearable placeholder="请输入AGV名称" />
        </el-form-item>
        <el-form-item label="工艺所处循环">
          <el-select
            v-model="getParams.cycle_location_id"
            clearable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in process_cycle_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="物料类型">
          <el-select
            v-model="getParams.material_type_id"
            clearable
            size="small"
            placeholder="请选择"
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in material_type_list"
              :key="item.id"
              :label="item.port_material_type_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="AGV类型">
          <el-select
            v-model="currentObj.rack_type_id"
            size="small"
            placeholder="请选择"
            clearable
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in rackTypeList"
              :key="item.id"
              :label="item.rack_type_name"
              :value="item.id"
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
        <el-button v-permission="['rack_info','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun(1)">新增</el-button>
        <el-button v-permission="['rack_info','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          label="AGV名称"
          min-width="14"
        >
          <template slot-scope="scope">{{ scope.row.rack_name }}</template>
        </el-table-column>
        <!-- <el-table-column
          label="是否一体车"
          min-width="15"
        >
          <template slot-scope="scope">{{ scope.row.is_bfi?'是':'否' }}</template>
        </el-table-column> -->
        <el-table-column
          prop="rack_type_name"
          label="AGV类型"
          min-width="16"
        />
        <el-table-column
          prop="rcs_agv_no"
          label="调度小车编号"
          width="100"
        />
        <el-table-column
          prop="cycle_location_name"
          label="所处循环"
          min-width="20"
        />
        <el-table-column
          prop="material_type_name"
          label="当前物料类型"
          min-width="21"
        />
        <el-table-column
          prop="platform_name"
          label="物料来源站台"
          min-width="21"
        />
        <el-table-column
          prop="diversion_platform_name"
          label="物料目标站台"
          min-width="21"
        />
        <el-table-column
          prop="recipe_time"
          label="物料工艺时间"
          width="150"
        />
        <!-- <el-table-column
          prop="is_locked"
          label="调度锁定状态"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.is_locked?'锁定':'解锁' }}</template>
        </el-table-column> -->
        <!-- <el-table-column
          prop="is_used"
          label="启用状态"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.is_used?'是':'否' }}</template>
        </el-table-column> -->
        <el-table-column
          prop="created_username"
          label="创建人"
          min-width="15"
        />
        <el-table-column
          prop="created_time"
          label="创建时间"
          width="150"
        />
        <el-table-column
          prop="last_update_username"
          label="修改人"
          min-width="15"
        />
        <el-table-column
          prop="last_updated_time"
          label="修改时间"
          width="150"
        />
        <el-table-column label="操作" width="120">
          <template slot-scope="{row}">
            <el-button v-permission="['rack_info','change']" size="small" type="text" @click="editShow(row,1)">修改</el-button>
            <el-button v-permission="['rack_info','change']" size="small" type="text" @click="editShow(row,2)">异常处理</el-button>
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
      :title="dialogType===1?(currentObj.id?'编辑':'新建')+'料架':'异常处理'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <div v-if="dialogType===1">
          <el-form-item label="AGV类型" prop="rack_type">
            <el-select
              v-model="currentObj.rack_type"
              size="small"
              placeholder="请选择"
              :disabled="currentObj.id?true:false"
              @change="changeRackType"
            >
              <el-option
                v-for="item in rackTypeList"
                :key="item.id"
                :label="item.rack_type_name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <!-- <el-form-item label="是否一体车">
            <span v-if="currentObj.rack_type&&currentObj.is_bfi">是</span>
            <span v-if="currentObj.rack_type&&!currentObj.is_bfi">否</span>
          </el-form-item> -->
          <el-form-item label="AGV名称" prop="rack_name">
            <!-- <el-select
              v-if="currentObj.is_bfi"
              v-model="currentObj.rack_name"
              clearable
              size="small"
              placeholder="请选择"
              :disabled="currentObj.id?true:false"
            >
              <el-option
                v-for="item in agvList"
                :key="item.id"
                :label="item.vehicle_name"
                :value="item.vehicle_name"
              />
            </el-select> -->
            <el-input v-model="currentObj.rack_name" :disabled="currentObj.id?true:false" size="small" />
          </el-form-item>
          <el-form-item label="工艺所处循环" prop="cycle_location">
            <el-select
              v-model="currentObj.cycle_location"
              clearable
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in process_cycle_list"
                :key="item.global_name"
                :label="item.global_name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="调度小车编号">
            <el-select
              v-model="currentObj.rcs_agv_info"
              clearable
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in rcs_list"
                :key="item.id"
                :disabled="item.mcs_agv!==null"
                :label="item.rcs_agv_id"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
        </div>
        <div v-if="dialogType===2">
          <el-form-item label="物料类型">
            <el-select
              v-model="currentObj.material_type"
              clearable
              size="small"
              placeholder="请选择"
              @change="changeMaterialType"
            >
              <el-option
                v-for="item in material_type_list"
                :key="item.id"
                :label="item.port_material_type_name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="物料来源站台">
            <el-select
              v-model="currentObj.platform"
              clearable
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in out_station_list"
                :key="item.id"
                :label="item.platform_name"
                :value="item.id"
                :disabled="!item.is_used"
              >
                <span style="float: left">{{ item.platform_name }}</span>
                <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px;margin-left:5px">已禁用</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="物料目标站台">
            <el-select
              v-model="currentObj.diversion_platform"
              clearable
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in in_station_list"
                :key="item.id"
                :label="item.platform_name"
                :value="item.id"
                :disabled="!item.is_used"
              >
                <span style="float: left">{{ item.platform_name }}</span>
                <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px;margin-left:5px">已禁用</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="物料工艺时间">
            <el-date-picker
              v-model="currentObj.recipe_time"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="选择日期"
              clearable
            />
          </el-form-item>
          <!-- <el-form-item label="调度锁定状态">
            <el-select
              v-model="currentObj.is_locked"
              size="small"
              placeholder="请选择"
              clearable
            >
              <el-option
                v-for="item in [{name:'锁定',label:true},{name:'解锁',label:false}]"
                :key="item.name"
                :label="item.name"
                :value="item.label"
              />
            </el-select>
          </el-form-item> -->
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { rackInfo, rackInfoDel } from '@/api/base_w'
import { getGlobalCodes } from '@/api/basics'
import { rackType, portMaterialType, platformInfo, rcsAgvInfo } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'RackManage',
  components: { page },
  data() {
    return {
      getParams: {},
      total: 0,
      loading: false,
      tableData: [],
      dialogVisible: false,
      currentObj: {},
      rules: {
        rack_type: [
          { required: true, message: '请选择AGV类型', trigger: 'change' }
        ],
        rack_name: [
          { required: true, message: '请填写AGV名称', trigger: 'blur' }
        ],
        cycle_location: [
          { required: true, message: '请选择工序所处循环', trigger: 'change' }
        ],
        is_locked: [
          { required: true, message: '请选择调度锁定状态', trigger: 'blur' }
        ],
        material_type: [
          { required: true, message: '请选择物料类型', trigger: 'blur' }
        ],
        platform: [
          { required: true, message: '请选择物料来源站台', trigger: 'blur' }
        ]
      },
      rackTypeList: [],
      rcs_list: [],
      process_cycle_list: [],
      agvList: [],
      btnLoading: false,
      dialogType: 1,
      material_type_list: [],
      out_station_list: [],
      in_station_list: [],
      currentVal: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await rackInfo('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getOtherList() {
      try {
        const a = await Promise.all([
          rackType('get', null, { params: { all: 1 }}),
          getGlobalCodes({ all: 1, type_name: '工艺循环' }),
          portMaterialType('get', null, { params: { all: 1 }}),
          rcsAgvInfo('get', null, { params: { all: 1 }})
        ])
        this.rackTypeList = a[0] || []
        this.process_cycle_list = a[1] || []
        this.material_type_list = a[2] || []
        this.rcs_list = a[3].data || []
      } catch (e) {
        //
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getOtherList()
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    changeMaterialType(id) {
      this.$set(this.currentObj, 'platform', '')
      this.$set(this.currentObj, 'diversion_platform', '')
      this.out_getPlatform(id)
      this.in_getPlatform(id)
    },
    async out_getPlatform(val) {
      try {
        const obj = {
          out_port_material_type: val,
          all: 1
        }
        const data = await platformInfo('get', null, { params: obj })
        this.out_station_list = data || []
      } catch (e) {
        //
      }
    },
    async in_getPlatform(val) {
      try {
        const obj = {
          in_port_material_type: val,
          all: 1
        }
        const data = await platformInfo('get', null, { params: obj })
        this.in_station_list = data || []
      } catch (e) {
        //
      }
    },
    changeRackType(val) {
      const obj = this.rackTypeList.find(d => d.id === val)
      this.currentObj.is_bfi = obj.is_bfi
    },
    addFun(num) {
      this.getOtherList()
      this.dialogType = num
      this.dialogVisible = true
    },
    editShow(row, num) {
      this.getOtherList()
      this.dialogType = num
      this.dialogVisible = true
      this.currentObj = JSON.parse(JSON.stringify(row))
      this.out_getPlatform(this.currentObj.material_type)
      this.in_getPlatform(this.currentObj.material_type)
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
      if (this.$refs.ruleForm) {
        this.$refs.ruleForm.resetFields()
      }
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
        rackInfoDel('post', null, { data: { obj_ids: arr }})
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
      if (this.dialogType === 2) {
        if (this.currentObj.material_type && !this.currentObj.platform) {
          this.$message('物料来源站台必填')
          return
        }
      }
      if (this.currentObj.is_locked === '') {
        delete this.currentObj.is_locked
      }
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await rackInfo(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.getList()
            this.handleClose(null)
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
