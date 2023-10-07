<template>
  <div>
    <!-- 分流配置 未使用-->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="原工艺">
          <el-select
            v-model="getParams.original_craft_id"
            clearable
            size="small"
            placeholder="请选择原工艺"
          >
            <el-option
              v-for="item in craft_list"
              :key="item.craft_desc"
              :label="item.craft_desc"
              :value="item.id"
            />
          </el-select>
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
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button type="modify" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          prop="original_craft_name"
          label="原工艺名称"
          min-width="20"
        />
        <el-table-column
          prop="new_craft_name"
          label="新工艺名称"
          min-width="20"
        />
        <el-table-column
          prop="stock_upper_limit"
          label="库存上限"
          min-width="20"
        />
        <el-table-column
          label="启用标志"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
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
      :title="(currentObj.id?'编辑':'新建')+'分流配置信息'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="原工艺" prop="original_craft">
          <el-select
            v-model="currentObj.original_craft"
            :disabled="currentObj.id?true:false"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in craft_list"
              :key="item.craft_desc"
              :label="item.craft_desc"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="新工艺" prop="new_craft">
          <el-select
            v-model="currentObj.new_craft"
            clearable
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in craft_list"
              :key="item.craft_desc"
              :label="item.craft_desc"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="库存上限" prop="stock_upper_limit">
          <el-input-number v-model="currentObj.stock_upper_limit" size="small" />
        </el-form-item><br>
        <!-- <el-form-item label="是否启用" prop="is_used">
          <el-radio v-model="currentObj.is_used" :label="true">是</el-radio>
          <el-radio v-model="currentObj.is_used" :label="false">否</el-radio>
        </el-form-item> -->

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="js">
import { craftManagements } from '@/api/base_w'
import { shuntConf, shuntConfUpdate, shuntConfDel } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'ShuntConfiguration',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      craft_list: [],
      dialogVisible: false,
      rules: {
        original_craft: [
          { required: true, message: '请选择原工艺', trigger: 'blur' }
        ],
        new_craft: [
          { required: true, message: '请选择新工艺', trigger: 'blur' }
        ],
        stock_upper_limit: [
          { required: true, message: '请填写库存上限', trigger: 'change' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    this.getDistrictList()
  },
  mounted() {
  },
  methods: {
    async getDistrictList() {
      try {
        const data = await craftManagements('get', null, { params: { all: 1 }})
        this.craft_list = data || []
      } catch (e) {
        //
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await shuntConf('get', null, { params: this.getParams })
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
        shuntConfDel('post', null, { data: { obj_ids: arr }})
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
        shuntConfUpdate('post', null, { data: { 'obj_ids': arr }})
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
            await shuntConf(_api, this.currentObj.id || null, { data: this.currentObj })
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
    }
  }
}
</script>

<style lang="scss" scoped>

</style>

