<template>
  <div v-loading="loading">
    <!-- 机台线别 -->
    <div class="grid-left">
      <h3>工序</h3>
      <el-tree default-expand-all :data="data" :props="defaultProps" highlight-current node-key="process_name" @node-click="handleNodeClick" />
    </div>
    <div class="grid-content">
      <div class="top-search-box">
        <el-form :inline="true">
          <el-form-item label="编号">
            <el-input v-model="getParams.line_code" size="small" clearable placeholder="编号" />
          </el-form-item>
          <el-form-item label="名称">
            <el-input v-model="getParams.line_name" size="small" clearable placeholder="名称" />
          </el-form-item>
          <el-form-item>
            <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="center-box">
        <div class="botton-box">
          <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
          <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
          <el-button type="modify" icon="el-icon-download" size="small" :loading="btnExportLoad" @click="exportFun">导出</el-button>
        </div>
        <el-table
          ref="multipleTable"
          :data="tableData"
          tooltip-effect="dark"
          style="width: 100%"
          stripe
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="40" />
          <el-table-column
            label="编号"
            min-width="20"
          >
            <template slot-scope="scope">{{ scope.row.line_code }}</template>
          </el-table-column>
          <el-table-column
            prop="line_name"
            label="名称"
            min-width="20"
            show-overflow-tooltip
          />
          <el-table-column
            label="物料类别"
            min-width="20"
            show-overflow-tooltip
          >
            <template slot-scope="scope">{{ scope.row.material_type }}</template>
          </el-table-column>
          <el-table-column
            prop="ordering"
            label="排序"
            min-width="10"
            show-overflow-tooltip
          />
          <el-table-column
            prop="process_name"
            label="所属工序"
            show-overflow-tooltip
            min-width="30"
          />
          <el-table-column
            label="小时产能"
            min-width="20"
            show-overflow-tooltip
          >
            <template slot-scope="scope">{{ scope.row.capacity }}</template>
          </el-table-column>
          <el-table-column label="操作" width="60">
            <template slot-scope="{row}">
              <el-button type="text" size="small" @click="editShow(row)">修改</el-button>
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
        width="500px"
        :before-close="handleClose"
        class="dialog-style"
      >
        <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
          <el-form-item label="编号" prop="line_code">
            <el-input v-model="currentObj.line_code" size="small" :disabled="currentObj.id?true:false" />
          </el-form-item>
          <el-form-item label="名称" prop="line_name">
            <el-input v-model="currentObj.line_name" size="small" :disabled="currentObj.id?true:false" />
          </el-form-item>
          <el-form-item label="排序" prop="ordering">
            <el-input v-model="currentObj.ordering" size="small" />
          </el-form-item>
          <el-form-item label="物料类别">
            <el-input v-model="currentObj.material_type" size="small" />
          </el-form-item>
          <el-form-item label="所属工序" prop="process">
            <el-select
              v-model="currentObj.process"
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
          <el-form-item label="小时产能">
            <el-input v-model="currentObj.capacity" size="small" />
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="handleClose(false)">取 消</el-button>
          <el-button :loading="btnLoading" type="primary" @click="submitFun">确 定</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import page from '@/components/page'
import { processSummary, equipLines, productionProcesses, equipLinesDel } from '@/api/base_w'
export default {
  name: 'DeviceLineType',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        line_code: [
          { required: true, message: '请填写编号', trigger: 'blur' }
        ],
        line_name: [
          { required: true, message: '请填写名称', trigger: 'blur' }
        ],
        ordering: [
          { required: true, message: '请填写排序', trigger: 'blur' }
        ]
      },
      currentVal: [],
      data: [],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      show: false,
      btnLoading: false,
      btnExportLoad: false,
      process_list: [],
      loading: true
    }
  },
  created() {
    this.getListRight()
    this.getListLeft()
    this.getProcessList()
  },
  mounted() {
  },
  methods: {
    async getListLeft() {
      try {
        this.loading = true
        const data = await processSummary('get')
        data.forEach(d => {
          d.label = d.process_name + '[' + d.count + ']'
        })
        this.data = [{
          label: '全部',
          children: data || []
        }]
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getListRight() {
      try {
        const data = await equipLines('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
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
    changeList() {
      this.getParams.page = 1
      this.getListRight()
      this.getListLeft()
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.dialogVisible = true
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getListLeft()
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.dialogVisible = true
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
      if (!this.currentVal) {
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
        equipLinesDel('post', null, { data: { obj_ids: arr }})
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
            await equipLines(_api, this.currentObj.id || null, { data: this.currentObj })
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
    handleNodeClick(val) {
      this.getParams.process_name = val.process_name
      this.getParams.page = 1
      this.getListRight()
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = equipLines
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
  .grid-left{
    border-bottom: 1px solid #eee;
    // padding-left:10px;

    transition: width 0.28s;
    width: 210px !important;
    background-color: #fff;
    height: 100%;
    position: fixed;
    font-size: 0px;
    top: 80px;
    bottom: 0;
    left:210px;
    overflow: hidden;
    border-right: 2px solid #eee;
    border-top: 2px solid #eee;

    h3{
      font-size: 17px;
      margin: 5px;
      margin-left: 10px;
    }
    .el-tree{
      overflow-y: scroll;
      height: 100%;
      margin-bottom: -19px;
      margin-right: -19px;
    }
  }
  .grid-content{
    margin-left:220px;
  }
</style>
