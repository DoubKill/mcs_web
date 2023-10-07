<template>
  <div>
    <!-- 设备部件管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="工序">
          <el-select
            v-model="getParams.process"
            clearable
            size="small"
            placeholder="请选择工序"
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
        <el-form-item label="设备">
          <el-select
            v-model="getParams.equip"
            clearable
            size="small"
            placeholder="请选择归属设备"
            @visible-change="visibleChange1"
          >
            <el-option
              v-for="item in equip_list"
              :key="item.equip_name"
              :label="item.equip_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部件类型">
          <el-select
            v-model="getParams.part_type"
            clearable
            size="small"
            placeholder="请选择部件类型"
          >
            <el-option
              v-for="item in type_list"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="部件号">
          <el-input v-model="getParams.part_code" size="small" clearable placeholder="请输入部件号" />
        </el-form-item>
        <el-form-item label="启用标志">
          <el-select
            v-model="getParams.is_used"
            clearable
            size="small"
            placeholder="请选择启用标志"
          >
            <el-option
              v-for="item in [{id:true,name:'启用'},{id:false,name:'禁用'}]"
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
        <el-button v-permission="['equip_parts','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['equip_parts','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['equip_parts','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['equip_parts','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
      </div>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        :span-method="objectSpanMethod"
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
          label="设备编号"
          min-width="15"
        />
        <el-table-column
          prop="equip_name"
          label="设备名称"
          min-width="15"
        />
        <el-table-column
          prop="process_name"
          label="工序"
          min-width="12"
        />
        <el-table-column
          prop="part_station_code"
          label="站台编号"
          min-width="20"
        />
        <el-table-column
          prop="part_station_name"
          label="站台名称"
          min-width="20"
        />
        <el-table-column
          prop="part_code"
          label="部件号"
          min-width="22"
        />
        <el-table-column
          prop="part_name"
          label="部件名称"
          min-width="19"
        />
        <el-table-column
          prop="part_type_name"
          label="部件类型"
          min-width="20"
        />
        <el-table-column
          prop="axis"
          label="轴号"
          min-width="10"
        />
        <el-table-column
          label="启用标志"
          min-width="15"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="threshold"
          label="阈值"
          min-width="10"
        />
        <el-table-column
          prop="delay_time"
          label="延时时间阈值"
          min-width="20"
        />
        <el-table-column label="操作" width="120">
          <template slot-scope="{row}">
            <el-button v-permission="['equip_parts','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
            <el-button v-permission="['equip_parts','change']" size="small" type="text" @click="editValue(row)">阈值设置</el-button>
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
      :title="(currentObj.id?'编辑':'新建')+'设备部件信息'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="站台" prop="part_station">
          <el-select
            v-model="currentObj.part_station"
            clearable
            size="small"
            placeholder="请选择"
            @change="changeText()"
            @visible-change="visibleChange2"
          >
            <el-option
              v-for="item in platform_list"
              :key="item.platform_name"
              :label="item.platform_name"
              :value="item.id"
              :disabled="!item.is_used"
            >
              <span style="float: left">{{ item.platform_name }}</span>
              <span v-if="!item.is_used" style="float: right; color: #8492a6; font-size: 13px">已禁用</span>
            </el-option>
          </el-select>
        </el-form-item><br>
        <el-form-item label="设备" prop="equip">
          <el-select
            v-model="currentObj.equip"
            disabled
            clearable
            size="small"
            placeholder=""
          >
            <el-option
              v-for="item in equip_list"
              :key="item.equip_name"
              :label="item.equip_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item label="部件编号" prop="part_code">
          <el-input v-model="currentObj.part_code" size="small" disabled />
        </el-form-item><br>
        <el-form-item label="部件名称" prop="part_name">
          <el-input v-model="currentObj.part_name" size="small" />
        </el-form-item><br>
        <el-form-item label="部件类型" prop="part_type">
          <el-select
            v-model="currentObj.part_type"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in type_list"
              :key="item.name"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item label="排" prop="row">
          <el-select
            v-model="currentObj.row"
            size="small"
            placeholder="请选择"
            @change="changeAxle"
          >
            <el-option
              v-for="item in [1,2]"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item label="列" prop="column">
          <el-select
            v-model="currentObj.column"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [1]"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item label="层" prop="layer">
          <el-select
            v-model="currentObj.layer"
            size="small"
            placeholder="请选择"
            @change="changeAxle"
          >
            <el-option
              v-for="item in [1,2]"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item label="轴号" prop="axis">
          <el-input v-model="currentObj.axis" disabled size="small" />
        </el-form-item><br>
        <el-form-item label="是否是单轴任务" prop="is_single_axis">
          <el-radio v-model="currentObj.is_single_axis" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_single_axis" :label="false">否</el-radio>
        </el-form-item><br>
        <!-- <el-form-item label="是否启用" prop="is_used">
          <el-radio v-model="currentObj.is_used" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_used" :label="false">否</el-radio>
        </el-form-item> -->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun(true)">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      :title="'阈值设置'"
      :visible.sync="dialogVisibleValue"
      width="500px"
      :before-close="handleCloseValue"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="部件编号" prop="part_code">
          <el-input v-model="currentObj.part_code" size="small" disabled />
        </el-form-item><br>
        <el-form-item label="部件名称" prop="part_name">
          <el-input v-model="currentObj.part_name" size="small" disabled />
        </el-form-item><br>
        <el-form-item label="阈值" prop="threshold">
          <el-input-number v-model="currentObj.threshold" size="small" />
        </el-form-item><br>
        <el-form-item label="任务延迟时间(S)" prop="delay_time">
          <el-input-number v-model="currentObj.delay_time" size="small" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleCloseValue(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun(false)">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="js">
import { basicsEquips, productionProcesses } from '@/api/base_w'
import { getGlobalCodes } from '@/api/basics'
import { platformInfo, equipParts, equipPartsUpdate, equipPartsDel } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'SparePartManage',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      process_list: [],
      currentObj: { is_single_axis: true },
      platform_list: [],
      equip_list: [],
      type_list: [{ name: '设备入货(AGV卸货)', id: 1 }, { name: '设备出货(AGV取货)', id: 2 }],
      dialogVisible: false,
      dialogVisibleValue: false,
      rules: {
        part_station: [
          { required: true, message: '请选择站台 ', trigger: 'change' }
        ],
        part_code: [
          { required: true, message: '请选择部件编号 ', trigger: 'change' }
        ],
        part_name: [
          { required: true, message: '请填写部件名称', trigger: 'blur' }
        ],
        part_type: [
          { required: true, message: '请选择部件类型', trigger: 'change' }
        ],
        row: [
          { required: true, message: '请选择排', trigger: 'change' }
        ],
        column: [
          { required: true, message: '请选择列', trigger: 'change' }
        ],
        layer: [
          { required: true, message: '请选择层', trigger: 'change' }
        ],
        axis: [
          { required: true, message: '请填写轴号', trigger: 'change' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    // this.getPlatform()
    // this.getProcessList()
    // this.getEquip()
  },
  mounted() {
  },
  methods: {
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if ([1, 2, 3].includes(columnIndex) && this.spanArr) {
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
      if ([4, 5].includes(columnIndex) && this.spanArr1) {
        const _row = this.spanArr1[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getProcessList()
      }
    },
    async getProcessList() {
      try {
        const data = await productionProcesses('get', null, { params: { all: 1 }})
        this.process_list = data || []
      } catch (e) {
        //
      }
    },
    visibleChange1(bool) {
      if (bool) {
        this.getEquip()
      }
    },
    async getEquip() {
      try {
        const data = await basicsEquips('get', null, { params: { all: 1, is_used: true }})
        this.equip_list = data.filter(d => d.is_used)
      } catch (e) {
        //
      }
    },
    async getType() {
      try {
        const data = await getGlobalCodes({ all: 1, type_name: '设备部件类型' })
        this.type_list = data || []
      } catch (e) {
        //
      }
    },
    visibleChange2(bool) {
      if (bool) {
        this.getPlatform()
      }
    },
    async getPlatform() {
      try {
        const data = await platformInfo('get', null, { params: { all: 1 }})
        this.platform_list = data || []
      } catch (e) {
        //
      }
    },
    async changeText() {
      const data = await platformInfo('get', this.currentObj.part_station, { params: {}})
      this.$set(this.currentObj, 'part_station_code', data.platform_code)
      this.$set(this.currentObj, 'equip', data.equip)
    },
    changeAxle() {
      if (!this.currentObj.part_station_code) {
        this.$message('请先选择站台')
        this.currentObj.row = null
        this.currentObj.layer = null
        return
      }
      if (this.currentObj.row && this.currentObj.layer) {
        this.$set(this.currentObj, 'part_code', this.currentObj.part_station_code + '_' + this.currentObj.row + '_' + this.currentObj.column + '_' + this.currentObj.layer)
        if (this.currentObj.row === 1) {
          this.$set(this.currentObj, 'axis', this.currentObj.layer === 1 ? 3 : 1)
        } else {
          this.$set(this.currentObj, 'axis', this.currentObj.layer === 1 ? 4 : 2)
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await equipParts('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.spanArr = []
        this.pos = null
        this.spanArr1 = []
        this.pos1 = null
        for (var i = 0; i < this.tableData.length; i++) {
          if (i === 0) {
            // 如果是第一条记录（即索引是0的时候），向数组中加入１
            this.spanArr.push(1)
            this.pos = 0
            this.spanArr1.push(1)
            this.pos1 = 0
          } else {
            if (this.tableData[i].equip_code === this.tableData[i - 1].equip_code) {
              // 如果a相等就累加，并且push 0  这里是根据一样的a匹配
              this.spanArr[this.pos] += 1
              this.spanArr.push(0)
            } else {
              // 不相等push 1
              this.spanArr.push(1)
              this.pos = i
            }
            if (this.tableData[i].part_station_code === this.tableData[i - 1].part_station_code) {
              // 如果a相等就累加，并且push 0  这里是根据一样的a匹配
              this.spanArr1[this.pos1] += 1
              this.spanArr1.push(0)
            } else {
              // 不相等push 1
              this.spanArr1.push(1)
              this.pos1 = i
            }
          }
        }
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.currentObj.column = 1
      this.currentObj.is_single_axis = true
      this.dialogVisible = true
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.$set(this.currentObj, 'equip', this.currentObj.equip_code)
      this.dialogVisible = true
      this.getPlatform()
      this.getProcessList()
      this.getEquip()
    },
    editValue(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisibleValue = true
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
      this.currentObj = { is_single_axis: true }
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleCloseValue(done) {
      this.dialogVisibleValue = false
      this.currentObj = { is_single_axis: true }
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
        equipPartsDel('post', null, { data: { obj_ids: arr }})
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
        equipPartsUpdate('post', null, { data: { 'obj_ids': arr }})
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
    submitFun(val) {
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
            await equipParts(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            if (val) {
              this.handleClose(null)
            } else {
              this.handleCloseValue(null)
            }
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

<style lang="scss" scoped>

</style>
