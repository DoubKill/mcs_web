<template>
  <div>
    <!-- 库存查询 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="库存设备">
          <el-input
            v-model="getParams.equip_name"
            size="small"
            clearable
            placeholder="请输入库存设备"
          />
        </el-form-item>
        <el-form-item label="设备类型">
          <el-select
            v-model="getParams.equip_type"
            clearable
            size="small"
            placeholder="请选择设备类型"
          >
            <el-option
              v-for="item in equipType_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="生产设备">
          <el-select
            v-model="getParams.production_equip"
            clearable
            size="small"
            placeholder="请输入生产设备"
          >
            <el-option
              v-for="item in equip_list1"
              :key="item.equip_name"
              :label="item.equip_name"
              :value="item.equip_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="生产工序">
          <el-select
            v-model="getParams.process"
            clearable
            size="small"
            placeholder="请选择生产工序"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.process_name"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            type="success"
            icon="el-icon-search"
            size="small"
            @click="changeList"
          >搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div
      v-loading="loading"
      class="center-box"
    >
      <!-- <div class="botton-box">
        <el-button
          type="blue"
          icon="el-icon-plus"
          size="small"
          @click="addFun"
        >新增</el-button>
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="small"
          @click="deleteFun"
        >删除</el-button>
        <el-button
          type="blue"
          icon="el-icon-s-grid"
          size="small"
          @click="stockLook"
        >在制库存</el-button>
      </div> -->
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        :span-method="objectSpanMethod"
        style="width: 100%"
        stripe
        :cell-style="cellStyle"
        @selection-change="handleSelectionChange"
      >
        <!-- <el-table-column
          type="selection"
          width="40"
        /> -->
        <el-table-column
          prop="equip_name"
          label="库存设备"
          min-width="20"
        />
        <el-table-column
          prop="state"
          label="AGV状态"
          min-width="18"
        />
        <el-table-column
          label="AGV电量(%)"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-progress
              v-if="scope.row.equip_type!==2"
              :text-inside="true"
              :stroke-width="20"
              :percentage="scope.row.battery_percentage"
              status="success"
            />
          </template>
        </el-table-column>
        <el-table-column
          prop="row"
          label="排"
          min-width="20"
        />
        <el-table-column
          prop="column"
          label="列"
          min-width="20"
        />
        <el-table-column
          prop="layer"
          label="层"
          min-width="20"
        />
        <el-table-column
          prop="basket_num"
          label="花篮数量"
          min-width="20"
        />
        <el-table-column
          prop="process"
          label="生产工序"
          min-width="20"
        />
        <el-table-column
          prop="production_equip"
          label="生产设备"
          min-width="20"
        />
        <el-table-column
          prop="output_time"
          label="下料时间"
          width="150"
        />
        <el-table-column
          prop="in_stock_time"
          label="入库时间"
          width="150"
        />
        <!-- <el-table-column
          label="操作"
          width="60"
        >
          <template slot-scope="{row}">
            <el-button
              size="small"
              type="text"
              @click="editShow(row)"
            >修改</el-button>
          </template>
        </el-table-column> -->
      </el-table>
    </div>

    <el-dialog
      :title="(currentObj.id?'编辑':'新建')+'库存'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form
        ref="ruleForm"
        :model="currentObj"
        :rules="rules"
        label-width="150px"
        inline
      >
        <el-form-item
          label="设备类型"
          prop="equip_type"
        >
          <el-select
            v-model="currentObj.equip_type"
            :disabled="currentObj.id?true:false"
            size="small"
            placeholder="请选择"
            @change="clearEquip"
          >
            <el-option
              v-for="item in equipType_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="设备名称"
          prop="equip_name"
        >
          <el-select
            v-model="currentObj.equip_name"
            :disabled="currentObj.id?true:false"
            size="small"
            placeholder="请选择"
            @change="setEquip"
            @visible-change="changeEquip"
          >
            <el-option
              v-for="item in equip_list"
              :key="currentObj.equip_type===1?item.vehicle_name:item.equip_name"
              :label="currentObj.equip_type===1?item.vehicle_name:item.equip_name"
              :value="currentObj.equip_type===1?item.vehicle_name:item.equip_name"
            />
          </el-select>
        </el-form-item>、
        <el-form-item label="设备编号">
          <el-input
            v-model="currentObj.equip_code"
            disabled
            size="small"
            placeholder=""
          />
        </el-form-item>
        <el-form-item
          label="设备部件"
          prop="part_code"
        >
          <el-select
            v-model="currentObj.part_code"
            :disabled="currentObj.id?true:false"
            size="small"
            placeholder="请选择"
            @visible-change="changePart"
          >
            <el-option
              v-for="item in part_list"
              :key="item.part_code"
              :label="item.part_code"
              :value="item.part_code"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="花篮数量"
          prop="basket_num"
        >
          <el-input-number
            v-model="currentObj.basket_num"
            size="small"
          />
        </el-form-item>
        <el-form-item
          label="超时时长"
          prop="timeout_duration"
        >
          <el-input-number
            v-model="currentObj.timeout_duration"
            size="small"
          />
        </el-form-item>
        <el-form-item label="工序名称">
          <el-select
            v-model="currentObj.process"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="生产设备"
        >
          <el-select
            v-model="currentObj.production_equip"
            :disabled="currentObj.id?true:false"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in equip_list1"
              :key="item.equip_name"
              :label="item.equip_name"
              :value="item.id"
            />
          </el-select>
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

    <el-dialog
      title="在制库存统计"
      :visible.sync="dialogVisibleStock"
      width="90%"
      :before-close="handleCloseStock"
      class="dialog-style"
    >
      <el-table
        :data="tableDataStock"
        tooltip-effect="dark"
        style="width: 100%;margin-bottom: 100px;"
        stripe
      >
        <!-- <el-table-column
          prop="vehicle_code"
          label="区域"
          min-width="20"
        /> -->
        <el-table-column
          prop="craft_name"
          label="工艺"
          min-width="20"
        />
        <el-table-column
          v-for="(item,_key) in header"
          :key="_key"
          min-width="20"
          :prop="item+'_cnt'"
          :label="item"
        />
      </el-table>
      <span
        slot="footer"
        class="dialog-footer"
      />
    </el-dialog>
  </div>
</template>

<script lang="js">
import { basicsEquips, productionProcesses } from '@/api/base_w'
import { stockInfo, stockInfoDel, equipParts, vehicleInfos, stockInfoUnderway } from '@/api/jqy'
export default {
  name: 'InventoryQuery',
  components: { },
  data() {
    return {
      tableData: [],
      tableDataStock: [],
      total: 0,
      getParams: {},
      currentObj: {},
      equip_list: [],
      equip_list1: [],
      part_list: [],
      equipType_list: [{ id: 1, global_name: 'AGV' }, { id: 2, global_name: '缓存站' }],
      dialogVisible: false,
      dialogVisibleStock: false,
      rules: {
        equip_type: [
          { required: true, message: '请选择设备类型', trigger: 'change' }
        ],
        basket_num: [
          { required: true, message: '请输入花篮数量', trigger: 'change' }
        ],
        equip_name: [
          { required: true, message: '请选择设备名称', trigger: 'change' }
        ],
        part_code: [
          { required: true, message: '请填写设备部件编号', trigger: 'change' }
        ],
        material_identify: [
          { required: true, message: '请选择物料识别', trigger: 'change' }
        ]
      },
      header: [],
      process_list: [],
      currentVal: [],
      btnLoading: false,
      loading: true,
      loadingStock: true
    }
  },
  created() {
    this.getList()
    this.getProcessList()
    this.getEquip()
  },
  mounted() {
  },
  methods: {
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if ([0].includes(columnIndex) && this.spanArr) {
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
    },
    async getProcessList() {
      try {
        const data = await productionProcesses('get', null, { params: { all: 1, is_used: true }})
        this.process_list = data || []
      } catch (e) {
        //
      }
    },
    async getEquip() {
      try {
        const data = await basicsEquips('get', null, { params: { all: 1, is_used: true, equip_type: 1 }})
        this.equip_list1 = data || []
      } catch (e) {
        //
      }
    },
    clearEquip() {
      this.currentObj = { equip_type: this.currentObj.equip_type }
    },
    setEquip() {
      if (this.currentObj.equip_type === 1) {
        this.$set(this.currentObj, 'equip', this.equip_list.find(d => this.currentObj.equip_name === d.vehicle_name).id)
        this.$set(this.currentObj, 'equip_code', this.equip_list.find(d => this.currentObj.equip_name === d.vehicle_name).vehicle_code)
      } else {
        this.$set(this.currentObj, 'equip', this.equip_list.find(d => this.currentObj.equip_name === d.equip_name).id)
        this.$set(this.currentObj, 'equip_code', this.equip_list.find(d => this.currentObj.equip_name === d.equip_name).equip_code)
      }
    },
    // 设备下拉 选1 的时候拉AGV列表，选2的时候拉设备列表
    async changeEquip(val) {
      if (val) {
        if (this.currentObj.equip_type) {
          if (this.currentObj.equip_type === 1) {
            const data = await vehicleInfos('get', null, { params: { all: 1, is_used: true }})
            this.equip_list = data || []
          } else {
            const data = await basicsEquips('get', null, { params: { all: 1, is_used: true }})
            this.equip_list = data || []
          }
        } else {
          this.$message('请先选择设备类型')
        }
      }
    },
    // 部件下拉 选1 的时候拉固定列表，选2的时候拉设备对应部件列表
    async changePart(val) {
      if (val) {
        if (this.currentObj.equip_type && this.currentObj.equip) {
          if (this.currentObj.equip_type === 1) {
            this.part_list = [{ part_code: '轴1' }, { part_code: '轴2' }, { part_code: '轴3' }, { part_code: '轴4' }]
          } else {
            const data = await equipParts('get', null, { params: { all: 1, is_used: true, equip: this.currentObj.equip }})
            this.part_list = data || []
          }
        } else {
          this.$message('请先选择设备类型和设备')
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await stockInfo('get', null, { params: this.getParams })
        this.tableData = data || []
        this.spanArr = []
        this.pos = null
        for (var i = 0; i < this.tableData.length; i++) {
          if (this.tableData[i].battery_percentage) {
            this.tableData[i].battery_percentage = Number(Math.round((this.tableData[i].battery_percentage * 100) * 100) / 100)
          }

          if (i === 0) {
            // 如果是第一条记录（即索引是0的时候），向数组中加入１
            this.spanArr.push(1)
            this.pos = 0
          } else {
            if (this.tableData[i].equip_name === this.tableData[i - 1].equip_name) {
              // 如果a相等就累加，并且push 0  这里是根据一样的a匹配
              this.spanArr[this.pos] += 1
              this.spanArr.push(0)
            } else {
              // 不相等push 1
              this.spanArr.push(1)
              this.pos = i
            }
          }
        }
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async stockLook() {
      try {
        this.dialogVisibleStock = true
        this.loadingStock = true
        const data = await stockInfoUnderway('get', null, { params: this.getParams })
        this.header = data.header
        this.tableDataStock = data.data || []
        this.spanArr1 = []
        this.pos1 = null
        for (var i = 0; i < this.tableDataStock.length; i++) {
          if (i === 0) {
            // 如果是第一条记录（即索引是0的时候），向数组中加入１
            this.spanArr1.push(1)
            this.pos1 = 0
          } else {
            if (this.tableDataStock[i].equip_code === this.tableDataStock[i - 1].equip_code) {
              // 如果a相等就累加，并且push 0  这里是根据一样的a匹配
              this.spanArr1[this.pos] += 1
              this.spanArr1.push(0)
            } else {
              // 不相等push 1
              this.spanArr1.push(1)
              this.pos1 = i
            }
          }
        }
        this.loadingStock = false
      } catch (e) {
        this.loadingStock = false
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
    handleCloseStock() {
      this.dialogVisibleStock = false
      this.tableDataStock = []
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
        stockInfoDel('post', null, { data: { obj_ids: arr }})
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
            await stockInfo(_api, this.currentObj.id || null, { data: this.currentObj })
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
    cellStyle({ row, column, rowIndex, columnIndex }) {
      var cc = 'state'
      if (row[cc]) {
        if (row[cc] === '任务' && columnIndex === 1) {
          return 'background: rgb(180,241,208)'
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>

</style>

