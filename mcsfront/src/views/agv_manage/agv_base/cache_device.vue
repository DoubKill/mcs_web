<template>
  <div>
    <!-- 缓存设备管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="设备">
          <el-select
            v-model="getParams.equip_id"
            size="small"
            placeholder="请选择"
            style="width:120px"
            clearable
            @visible-change="visibleChange"
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.equip_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="工艺">
          <el-select
            v-model="getParams.a"
            size="small"
            placeholder="请选择"
            style="width:120px"
          >
            <el-option
              v-for="item in device_list"
              :key="item.process_name"
              :label="item.process_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item> -->
        <el-form-item label="工序">
          <el-select
            v-model="getParams.process_id"
            clearable
            size="small"
            placeholder="请选择"
            style="width:120px"
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
        <!-- <el-form-item label="物料标识">
          <el-select
            v-model="getParams.material_identify_id"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in ItemIDList"
              :key="item.id"
              :label="item.identify_code"
              :value="item.id"
            />
          </el-select>
        </el-form-item> -->
        <el-form-item label="启用标志">
          <el-select
            v-model="getParams.is_used"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
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
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['cache_device_conf','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['cache_device_conf','export']" type="blue" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
        <el-button v-permission="['cache_device_conf','update']" type="danger" icon="el-icon-turn-off" size="small" @click="openFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['cache_device_conf','update']" type="danger" icon="el-icon-open" size="small" @click="openFun('启用',1)">启用</el-button>
        <el-button v-permission="['cache_device_conf','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          label="设备编码"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.cache_device_code }}</template>
        </el-table-column>
        <el-table-column
          prop="cache_device_name"
          label="设备名称"
          min-width="20"
        />
        <!-- <el-table-column
          prop="device_type_name"
          label="缓存类型"
          min-width="20"
        />
        <el-table-column
          label="当前模式"
          width="120"
        >
          <template slot-scope="scope">
            <div v-if="scope.row.current_models">
              <div v-for="(item,index) in scope.row.current_models.split('/')" :key="index">{{ '第'+(index+1)+'层: ' }}{{ item }}</div>
            </div>
          </template>
        </el-table-column> -->
        <!-- <el-table-column
          prop="craft_desc"
          label="工艺"
          min-width="20"
        /> -->
        <el-table-column
          prop="process_name"
          label="工序"
          min-width="20"
        />
        <el-table-column
          prop="layer_num"
          label="层数"
          min-width="20"
        />
        <el-table-column
          prop="row_num"
          label="排数"
          min-width="20"
        />
        <el-table-column
          prop="column_num"
          label="列数"
          min-width="20"
        />
        <el-table-column
          prop="storage_num"
          label="库位可存放花篮数"
          min-width="20"
        />
        <el-table-column
          prop="in_threshold_nums"
          label="进堆栈阈值车数"
          min-width="20"
        />
        <el-table-column
          prop="out_threshold_nums"
          label="出堆栈阈值车数"
          min-width="20"
        />
        <!-- <el-table-column
          prop="material_identify_code"
          label="物料标识"
          min-width="20"
        /> -->
        <el-table-column
          label="启用标志"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'已启用':'已禁用' }}</el-tag>
          </template>
        </el-table-column>
        <!-- <el-table-column
          prop="cache_lower_limit"
          label="缓存下限(出库)"
          min-width="25"
          show-overflow-tooltip
        />
        <el-table-column
          prop="cache_upper_limit"
          label="缓存上限(入库)"
          show-overflow-tooltip
          min-width="25"
        /> -->
        <!-- <el-table-column
          prop="ply_nums"
          label="缓存层数"
          show-overflow-tooltip
          min-width="20"
        /> -->
        <el-table-column label="操作" width="120">
          <template slot-scope="{row}">
            <el-button v-permission="['cache_device_conf','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
            <!-- <el-button v-permission="['cache_device_conf','change']" size="small" type="text" @click="modeShow(row)">模式调整</el-button> -->
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
      :title="isMode?'模式调整':currentObj.id?'编辑':'新建'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <div v-if="!isMode">
          <el-form-item label="设备" prop="equip">
            <el-select
              v-if="currentObj.id"
              v-model="currentObj.cache_device_name"
              size="small"
              placeholder="请选择"
              :disabled="currentObj.id?true:false"
              @change="changeDevice"
            >
              <el-option
                v-for="item in device_list"
                :key="item.id"
                :label="item.equip_name"
                :value="item.id"
                :disabled="!item.is_used"
              />
            </el-select>
            <el-select
              v-else
              v-model="currentObj.equip"
              size="small"
              placeholder="请选择"
              :disabled="currentObj.id?true:false"
              @change="changeDevice"
            >
              <el-option
                v-for="item in device_list"
                :key="item.id"
                :label="item.equip_name"
                :value="item.id"
                :disabled="!item.is_used"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="工序" prop="">
            {{ currentObj.process_name }}
          </el-form-item>
          <!-- <el-form-item label="缓存层数" prop="">
            {{ currentObj.cache_levels }}
          </el-form-item> -->
          <!-- <el-form-item label="工艺" prop="craft">
            <el-select
              v-model="currentObj.craft"
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in craftList"
                :key="item.id"
                :label="item.craft_desc"
                :value="item.id"
              />
            </el-select>
          </el-form-item> -->
          <!-- <el-form-item label="物料标识" prop="material_identify">
            <el-select
              v-model="currentObj.material_identify"
              size="small"
              placeholder="请选择"
            >
              <el-option
                v-for="item in ItemIDList"
                :key="item.id"
                :label="item.identify_code"
                :value="item.id"
              />
            </el-select>
          </el-form-item> -->
          <el-form-item label="层数" prop="layer_num">
            <el-input-number v-model="currentObj.layer_num" size="small" controls-position="right" :min="1" />
          </el-form-item>
          <el-form-item label="排数" prop="row_num">
            <el-input-number v-model="currentObj.row_num" size="small" controls-position="right" :min="1" />
          </el-form-item>
          <el-form-item label="列数" prop="column_num">
            <el-input-number v-model="currentObj.column_num" size="small" controls-position="right" :min="1" />
          </el-form-item>
          <el-form-item label="库位可存放花篮数" prop="storage_num">
            <el-input-number v-model="currentObj.storage_num" size="small" controls-position="right" :min="1" />
          </el-form-item>
          <el-form-item label="进堆栈阈值车数" prop="in_threshold_nums">
            <el-input-number v-model="currentObj.in_threshold_nums" size="small" controls-position="right" :min="0" />
          </el-form-item>
          <el-form-item label="出堆栈阈值车数" prop="out_threshold_nums">
            <el-input-number v-model="currentObj.out_threshold_nums" size="small" controls-position="right" :min="0" />
          </el-form-item>
          <!-- <el-form-item label="缓存下限(出库)" prop="cache_lower_limit">
            <el-input-number v-model="currentObj.cache_lower_limit " size="small" controls-position="right" :min="0" />
          </el-form-item>
          <el-form-item label="缓存上限(入库)" prop="cache_upper_limit">
            <el-input-number v-model="currentObj.cache_upper_limit" size="small" controls-position="right" :min="0" />
          </el-form-item> -->
          <!-- <el-form-item label="缓存层数">
            <el-input-number v-model="currentObj.frequency" size="small" controls-position="right" :min="0" />
          </el-form-item> -->
        </div>
        <div v-else>
          <el-form-item label="设备编码" prop="">
            <el-input v-model="currentObj.cache_device_code" size="small" :disabled="currentObj.id?true:false" />
          </el-form-item>
          <el-form-item label="缓存类型" prop="">
            {{ currentObj.device_type_name }}
          </el-form-item>
          <el-form-item v-for="item in currentObj.cache_levels" :key="item" :label="`第${item}层模式`" prop="bit_signal">
            <el-radio v-model="currentObj._model[item-1]" label="正常模式">正常模式</el-radio>
            <el-radio v-model="currentObj._model[item-1]" label="存储模式">存储模式</el-radio>
          </el-form-item>
          <!-- <el-form-item label="模式" prop="bit_signal">
            <el-radio v-model="currentObj.is_locked" :label="true">正常模式</el-radio>
            <el-radio v-model="currentObj.is_locked" :label="false">存储模式</el-radio>
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
import { cacheDeviceConf, cacheDeviceConfDel, cacheDeviceConfUpdate, productionProcesses, basicsEquips } from '@/api/base_w'
// import { materialIdentifies } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'CacheDevice',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        equip: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        layer_num: [
          { required: true, message: '请填写层数', trigger: 'blur' }
        ],
        row_num: [
          { required: true, message: '请填写排数', trigger: 'blur' }
        ],
        column_num: [
          { required: true, message: '请填写列数', trigger: 'blur' }
        ],
        storage_num: [
          { required: true, message: '请填写库位可存放花篮数', trigger: 'blur' }
        ],
        in_threshold_nums: [
          { required: true, message: '请填写进堆栈阈值车数', trigger: 'blur' }
        ],
        out_threshold_nums: [
          { required: true, message: '请填写出堆栈阈值车数', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      exportLoading: false,
      resetLoading: false,
      device_list: [],
      process_list: [],
      // craftList: [],
      // ItemIDList: [],
      isMode: false
    }
  },
  created() {
    this.getList()
    // this.getOtherList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await cacheDeviceConf('get', null, { params: this.getParams })
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
          productionProcesses('get', null, { params: { all: 1 }}),
          basicsEquips('get', null, { params: { all: 1, equip_type: 2 }})
          // materialIdentifies('get', null, { params: { all: 1 }}),
          // craftManagements('get', null, { params: { all: 1 }})
        ])
        this.process_list = a[0] || []
        this.device_list = a[1].filter(d => d.is_used)
        // this.ItemIDList = a[2] || []
        // this.craftList = a[3] || []
      } catch (e) {
        //
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getOtherList()
      }
    },
    changeDevice(id) {
      const arr = this.device_list.filter(d => d.id === id)
      if (arr.length > 0) {
        const obj = arr[0]
        this.currentObj.process_name = obj.process__process_name
        this.currentObj.cache_levels = obj.ply_nums
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.getOtherList()
      this.dialogVisible = true
    },
    editShow(row) {
      this.getOtherList()
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
    },
    modeShow(row) {
      this.currentObj = Object.assign({}, row)
      let arr = []
      if (this.currentObj.current_models) {
        arr = this.currentObj.current_models.split('/')
      }
      for (let index = 0; index < this.currentObj.cache_levels; index++) {
        const d = index
        if (!arr[d]) {
          arr[d] = '正常模式'
        }
      }
      this.$set(this.currentObj, '_model', arr)
      this.isMode = true
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
      setTimeout(d => {
        this.isMode = false
      })
      if (done) {
        done()
      }
    },
    openFun(val, bool) {
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
        cacheDeviceConfUpdate('post', null, { data: { 'operation_type': bool, 'obj_ids': arr }})
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
        cacheDeviceConfDel('post', null, { data: { obj_ids: arr }})
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
      if (this.currentObj._model) {
        this.currentObj.current_models = this.currentObj._model.join('/')
      }
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            if (!this.currentObj.current_models) {
              this.currentObj.current_models = '正常模式/正常模式'
            }
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await cacheDeviceConf(_api, this.currentObj.id || null, { data: this.currentObj })
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
      this.exportLoading = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = cacheDeviceConf
      this.$store.dispatch('settings/operateTypeSetting', '导出')
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.exportLoading = false
        }).catch(e => {
          this.exportLoading = false
        })
    }
  }
}
</script>

      <style lang="scss" scoped>

      </style>

