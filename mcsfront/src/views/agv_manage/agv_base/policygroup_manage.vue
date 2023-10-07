<template>
  <div>
    <!-- 策略组管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="策略组名称">
          <el-input v-model="getParams.strategy_group_name" size="small" clearable placeholder="请输入策略组名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['strategy_groups','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['strategy_groups','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteTableFun">删除</el-button>
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
          label="策略组名称"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.strategy_group_name }}</template>
        </el-table-column>
        <el-table-column
          label="已选择搬运策略"
          min-width="40"
        >
          <template slot-scope="scope">
            <div v-for="item in scope.row.group_strategies" :key="item.id"> {{ item.strategy_name }}</div>
          </template>
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
        <el-table-column label="操作" width="120">
          <template slot-scope="{row}">
            <el-button v-permission="['strategy_groups','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
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
      :title="(currentObj.id?'编辑':'新建')+'策略组'"
      :visible.sync="dialogVisible"
      width="600px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" label-width="">
        <el-form-item label="策略组名称" prop="strategy_group_name">
          <el-input v-model="currentObj.strategy_group_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
      </el-form>
      <el-table
        :data="tableData1"
        tooltip-effect="dark"
        style="width: 100%"
        stripe
      >
        <el-table-column
          label="顺序"
          type="index"
          width="50"
        />
        <el-table-column
          label="搬运策略"
          min-width="30"
        >
          <template slot-scope="scope">
            <el-select
              v-model="scope.row.strategy"
              size="small"
              placeholder="请选择"
              clearable
              @visible-change="visibleChange"
            >
              <el-option
                v-for="item in strategyList"
                :key="item.id"
                :label="item.global_name"
                :value="item.id"
                :disabled="item.isSelect"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column
          label="是否模拟运行"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-radio v-model="scope.row.is_debug" :label="true">是</el-radio>
            <el-radio v-model="scope.row.is_debug" :label="false">否</el-radio>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun(scope.row,scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="text-align: center;">
        <el-button type="primary" size="small" @click="addDialogFun">插入一行</el-button>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import page from '@/components/page'
import { strategyGroups } from '@/api/jqy'
import { strategyGroupsDel } from '@/api/base_w'
import { getGlobalCodes } from '@/api/basics'
export default {
  name: 'PolicyGroupManage',
  components: { page },
  data() {
    return {
      getParams: {},
      tableData: [],
      loading: false,
      total: 0,
      dialogVisible: false,
      tableData1: [],
      currentObj: {},
      btnLoading: false,
      strategyList: [],
      currentVal: []
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
        const data = await strategyGroups('get', null, { params: this.getParams })
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
          getGlobalCodes({ all: 1, type_name: '搬运策略' })
        ])
        this.strategyList = a[0] || []
      } catch (e) {
        //
      }
    },
    addFun() {
      this.getOtherList()
      this.dialogVisible = true
    },
    editShow(row) {
      this.getOtherList()
      this.tableData1 = row.group_strategies || []
      this.currentObj.strategy_group_name = row.strategy_group_name
      this.currentObj.id = row.id
      this.dialogVisible = true
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
    visibleChange(bool) {
      if (bool) {
        this.strategyList.forEach(d => {
          const _index = this.tableData1.findIndex(D => D.strategy === d.id)
          if (_index > -1) {
            this.$set(d, 'isSelect', true)
          } else {
            this.$set(d, 'isSelect', false)
          }
        })
      }
    },
    deleteFun(row, index) {
      this.tableData1.splice(index, 1)
    },
    addDialogFun() {
      this.tableData1.push({ is_debug: false })
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      this.tableData1 = []
      if (done) {
        done()
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    deleteTableFun() {
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
        strategyGroupsDel('post', null, { data: { obj_ids: arr }})
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
      if (!this.currentObj.strategy_group_name) {
        this.$message('请填写策略组名称')
        return
      }
      const arr = []
      this.tableData1.forEach((d, i) => {
        if (d.strategy) {
          arr.push(d)
        }
        d.sn = i + 1
      })
      if (!arr.length) {
        this.$message('请添加策略')
        return
      }
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            const obj = {
              group_strategies: arr,
              strategy_group_name: this.currentObj.strategy_group_name
            }
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await strategyGroups(_api, this.currentObj.id || null, { data: obj })
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
    }
  }
}
</script>
