<template>
  <div>
    <!-- 休息区设置 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="编号">
          <el-input v-model="getParams.a" size="small" clearable placeholder="请输入编号0-9999" />
        </el-form-item>
        <el-form-item label="货架">
          <el-input v-model="getParams.area_code" size="small" clearable placeholder="货架号" />
        </el-form-item>
        <el-form-item label="工段">
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
        <el-form-item label="启用状态">
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
        <el-form-item label="锁定状态">
          <el-select
            v-model="getParams.is_locked"
            style="width:120px"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{id:true,name:'锁定'},{id:false,name:'解锁'}]"
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
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="success" icon="el-icon-download" size="small" @click="exportFun">导出</el-button>
        <el-upload
          style="margin:0 8px;display:inline-block"
          action="string"
          accept=".xls, .xlsx"
          :http-request="Upload"
          :show-file-list="false"
        >
          <el-button type="warning" size="small">导入Excel</el-button>
        </el-upload>

        <el-button type="danger" icon="el-icon-turn-off" size="small" @click="deleteFun('禁用',1)">禁用</el-button>
        <el-button type="modify" icon="el-icon-open" size="small" @click="deleteFun('启用',1)">启用</el-button>
        <el-button type="danger" icon="el-icon-lock" size="small" @click="deleteFun('锁定',2)">锁定</el-button>
        <el-button type="modify" icon="el-icon-unlock" size="small" @click="deleteFun('解锁',2)">解锁</el-button>
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
          prop="area_code"
          label="名称"
          min-width="20"
        />
        <el-table-column
          label="启用"
          width="60"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="锁定"
          width="60"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_locked?'':'info'">{{ scope.row.is_locked?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="locked_time"
          label="锁定时间s"
          min-width="20"
        />
        <el-table-column
          prop="current_shelve_code"
          label="当前货架"
          min-width="20"
        />
        <el-table-column
          label="物料标识"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.material_identify_name }}</template>
        </el-table-column>
        <el-table-column
          prop="shelve_time"
          label="货架时间s"
          min-width="20"
        />
        <el-table-column
          prop="shelve_state"
          label="货架状态"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="shelve_origin"
          label="货架来源"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="shelve_going"
          label="货架去向"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="target_equip_line_code"
          label="目标/优先机台"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="shelve_task_no"
          label="货架任务"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button size="small" type="text" @click="editShow(row)">修改</el-button>
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
      width="800px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="休息区名称" prop="area_code">
          <el-input v-model="currentObj.area_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item><br>
        <el-form-item label="是否启用" prop="is_used">
          <el-radio v-model="currentObj.is_used" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_used" :label="false">否</el-radio>
        </el-form-item>
        <el-form-item label="是否锁定" prop="is_locked">
          <el-radio v-model="currentObj.is_locked" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_locked" :label="false">否</el-radio>
        </el-form-item>
        <el-form-item label="锁定时间s">
          <el-input-number v-model="currentObj.locked_time" size="small" controls-position="right" :min="0" />
        </el-form-item><br>
        <el-form-item label="当前货架号">
          <el-input v-model="currentObj.current_shelve_code" size="small" />
        </el-form-item>
        <el-form-item label="物料标识">
          <el-input v-model="currentObj.material_identify_name" size="small" />
        </el-form-item>
        <el-form-item label="货架时间s">
          <el-input-number v-model="currentObj.shelve_time" size="small" controls-position="right" :min="0" />
        </el-form-item><br>
        <el-form-item label="货架状态">
          <el-input v-model="currentObj.shelve_state" size="small" />
        </el-form-item>
        <el-form-item label="货架来源">
          <el-input v-model="currentObj.shelve_origin" size="small" />
        </el-form-item>
        <el-form-item label="货架去向">
          <el-input v-model="currentObj.shelve_going" size="small" />
        </el-form-item>
        <el-form-item label="目标/优先机台编号">
          <el-input v-model="currentObj.target_equip_line_code" size="small" />
        </el-form-item>
        <el-form-item label="货架任务">
          <el-input v-model="currentObj.shelve_task_no" size="small" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="js">
import { restArea, batchUpdate, restAreaImportXlsx } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'RestAreaSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        area_code: [
          { required: true, message: '请填写货架号', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await restArea('get', null, { params: this.getParams })
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
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
    },
    resetFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
    },
    synchroFun() {},
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
    deleteFun(val, bool) {
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
        } else if (val === '锁定' && !d.is_locked) {
          arr.push(d.id)
        } else if (val === '解锁' && d.is_locked) {
          arr.push(d.id)
        }
      })
      this.$confirm(`此操作${val}, 是否继续?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        batchUpdate('post', null, { data: { 'operation_type': bool, 'obj_ids': arr }})
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
            await restArea(_api, this.currentObj.id || null, { data: this.currentObj })
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
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = restArea
      _api('get', null, { params: obj })
        .then(res => {
          window.open(process.env.VUE_APP_URL + res.url, '_self')
          this.btnExportLoad = false
        }).catch(e => {
          this.btnExportLoad = false
        })
    },
    Upload(param) {
      const formData = new FormData()
      formData.append('file', param.file)
      restAreaImportXlsx('post', null, { data: formData }).then(response => {
        this.$message({
          type: 'success',
          message: response
        })
        this.changeList()
      })
    }
  }
}
</script>

<style lang="scss" scoped>

</style>

