<template>
  <div>
    <!-- 物料类型管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="物料类型名称">
          <el-input v-model="getParams.port_material_type_name" size="small" clearable placeholder="物料类型名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['port_material_type','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['port_material_type','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <!-- <el-button type="modify" icon="el-icon-download" size="small" @click="exportFun">导出</el-button> -->
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
          prop="port_material_type_name"
          label="物料类型名称"
          min-width="20"
        />
        <el-table-column
          prop="desc"
          label="备注"
          min-width="20"
        />
        <el-table-column
          prop="q_time"
          label="Qtime超时阈值(分)"
          min-width="20"
        />
        <el-table-column
          prop="task_threshold_time"
          label="Qtime任务阈值(分)"
          min-width="20"
        />
        <!-- <el-table-column
          prop="cycle_location_name"
          label="工艺所处循环"
          min-width="20"
        /> -->
        <el-table-column
          prop="basket_type"
          label="花篮类型"
          min-width="10"
          :formatter="(row)=>{
            let obj = basketTypeList.find(d=>d.id === row.basket_type)
            return obj.name
          }"
        >
          <!-- <template slot-scope="scope"> -->
          <!-- <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_full?'':'info'">{{ scope.row.is_full?'是':'否' }}</el-tag> -->
          <!-- </template> -->
        </el-table-column>
        <el-table-column
          prop="created_username"
          label="创建人"
          min-width="20"
        />
        <el-table-column
          prop="created_time"
          label="创建时间"
          min-width="20"
        />
        <el-table-column
          prop="last_update_username"
          label="修改人"
          min-width="20"
        />
        <el-table-column
          prop="last_updated_time"
          label="修改时间"
          min-width="20"
        />
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button v-permission="['port_material_type','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
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
      width="600px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="200px">
        <el-form-item label="物料类型名称" prop="port_material_type_name">
          <el-input v-model="currentObj.port_material_type_name" size="small" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-color-picker v-model="currentObj.color" />
        </el-form-item>
        <el-form-item label="备注" prop="desc">
          <el-input v-model="currentObj.desc" size="small" />
        </el-form-item>
        <!-- <el-form-item label="工艺所处循环" prop="cycle_location">
          <el-select
            v-model="currentObj.cycle_location"
            clearable
            size="small"
            placeholder="请选择工艺所处循环"
          >
            <el-option
              v-for="item in cycle_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item> -->
        <el-form-item label="Qtime超时阈值(分钟)" prop="q_time">
          <el-input-number v-model="currentObj.q_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="Qtime任务阈值(分钟)" prop="task_threshold_time">
          <el-input-number v-model="currentObj.task_threshold_time" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="花篮类型" prop="basket_type">
          <el-select
            v-model="currentObj.basket_type"
            clearable
            size="small"
            placeholder="请选择花篮类型"
          >
            <el-option
              v-for="item in basketTypeList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
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
import { getGlobalCodes } from '@/api/basics'
import { portMaterialType, portMaterialTypeDel } from '@/api/jqy'
import page from '@/components/page'
import common from '@/utils/common'
export default {
  name: 'MaterialType',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      cycle_list: [],
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        port_material_type_name: [
          { required: true, message: '请填写物料类型名称', trigger: 'blur' }
        ],
        cycle_location: [
          { required: true, message: '请选择工艺所处循环', trigger: 'blur' }
        ],
        q_time: [
          { required: true, message: '请输入Qtime超时阈值', trigger: 'change' }
        ],
        task_threshold_time: [
          { required: true, message: '请输入Qtime任务阈值', trigger: 'change' }
        ],
        is_full: [
          { required: true, message: '必填项', trigger: 'change' }
        ],
        color: [
          { required: true, message: '必填项', trigger: 'change' }
        ],
        basket_type: [
          { required: true, message: '必填项', trigger: 'change' }
        ]
      },
      currentVal: [],
      basketTypeList: common.basketTypeList,
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    this.getCycle()
  },
  methods: {
    async getCycle() {
      try {
        const data = await getGlobalCodes({ all: 1, type_name: '工艺循环' })
        this.cycle_list = data || []
      } catch (e) {
        //
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await portMaterialType('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.dialogVisible = true
      this.currentObj = { is_full: true }
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
        portMaterialTypeDel('post', null, { data: { obj_ids: arr }})
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
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await portMaterialType(_api, this.currentObj.id || null, { data: this.currentObj })
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
      const _api = portMaterialType
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

  </style>

