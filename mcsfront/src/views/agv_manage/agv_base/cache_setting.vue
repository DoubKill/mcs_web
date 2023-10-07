<template>
  <div>
    <!-- 位置点管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="缓存位编号">
          <el-input v-model="getParams.location_code" size="small" clearable placeholder="请输入缓存位编号" />
        </el-form-item>
        <el-form-item label="类别">
          <el-select
            v-model="getParams.location_type"
            clearable
            size="small"
            placeholder="请选择类别"
          >
            <el-option
              v-for="item in type_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="当前AGV">
          <el-select
            v-model="getParams.rack_info_id"
            clearable
            size="small"
            placeholder="请选择当前AGV"
            @visible-change="getRack"
          >
            <el-option
              v-for="item in rack_list"
              :key="item.rack_name"
              :label="item.rack_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="锁定AGV">
          <el-select
            v-model="getParams.locked_rack_info_id"
            clearable
            size="small"
            placeholder="请选择锁定AGV"
            @visible-change="getRack"
          >
            <el-option
              v-for="item in rack_list"
              :key="item.rack_name"
              :label="item.rack_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
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
          <!-- <el-button type="success" size="small" @click="clearSearch">重置查询条件</el-button> -->
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
          <el-button v-permission="['cache_locations', 'sync']" type="success" size="small" :loading="btnExportLoad1" @click="onSubmit">同步位置点</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['cache_locations','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['cache_locations','export']" type="blue" icon="el-icon-download" size="small" :loading="btnExportLoad" @click="exportFun">导出</el-button>
        <el-button v-permission="['cache_locations','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['cache_locations','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['cache_locations','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          prop="location_code"
          label="缓存位编号"
          min-width="20"
        />
        <el-table-column
          prop="location_type_name"
          label="类别"
          min-width="20"
        />
        <el-table-column
          prop="rack_info_name"
          label="当前AGV"
          min-width="20"
        />
        <el-table-column
          prop="arrived_time"
          label="到位时间"
          min-width="25"
        />
        <el-table-column
          prop="lock_rack_info_name"
          label="锁定AGV"
          min-width="20"
        />
        <el-table-column
          prop="locked_time"
          label="锁定时间"
          min-width="25"
        />
        <!-- <el-table-column
          prop="district_code"
          label="所在区域编号"
          min-width="20"
        />
        <el-table-column
          prop="district_name"
          label="所在区域名称"
          min-width="20"
        /> -->
        <el-table-column
          label="启用标志"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_username"
          label="创建人"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="created_time"
          label="创建时间"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="last_update_username"
          label="修改人"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="last_updated_time"
          label="修改时间"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column label="操作" width="120">
          <template slot-scope="{row}">
            <el-button v-permission="['cache_locations','change']" size="small" type="text" @click="editShow(row,true)">编辑</el-button>
            <el-button v-permission="['cache_locations','change']" size="small" type="text" @click="editShow(row,false)">异常处理</el-button>
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
      :title="(currentObj.id?'编辑':'新建')+'缓存位'"
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="缓存位编号" prop="location_code">
          <el-input v-model="currentObj.location_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item><br>
        <el-form-item label="类别" prop="location_type">
          <el-select
            v-model="currentObj.location_type"
            clearable
            size="small"
            placeholder="请选择类别"
          >
            <el-option
              v-for="item in type_list"
              :key="item.global_name"
              :label="item.global_name"
              :value="item.id"
            />
          </el-select>
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
      title="异常处理"
      :visible.sync="dialogVisible1"
      width="500px"
      :before-close="handleClose1"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="当前AGV">
          <el-select
            v-model="currentObj.rack_info"
            clearable
            size="small"
            placeholder="请选择当前AGV"
          >
            <el-option
              v-for="item in rack_list"
              :key="item.rack_name"
              :label="item.rack_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item><br>
        <el-form-item
          label="到位时间"
          prop="arrived_time"
        >
          <el-date-picker
            v-model="currentObj.arrived_time"
            size="small"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="锁定AGV">
          <el-select
            v-model="currentObj.locked_rack_info"
            clearable
            size="small"
            placeholder="请选择锁定AGV"
          >
            <el-option
              v-for="item in rack_list"
              :key="item.rack_name"
              :label="item.rack_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="锁定时间"
          prop="locked_time"
        >
          <el-date-picker
            v-model="currentObj.locked_time"
            size="small"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose1(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun(false)">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="js">
import { rackInfo } from '@/api/base_w'
import { cacheLocations, cacheLocationsUpdate, cacheLocationsDel, syncLocations } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'CacheSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: { location_type: null },
      btnExportLoad: false,
      btnExportLoad1: false,
      dialogVisible: false,
      dialogVisible1: false,
      rules: {
        location_code: [
          { required: true, message: '请填写缓存位编号', trigger: 'blur' }
        ],
        location_type: [
          { required: true, message: '请选择类别', trigger: 'change' }
        ],
        district: [
          { required: true, message: '请选择区域', trigger: 'change' }
        ]
      },
      type_list: [
        { id: 1, global_name: '缓存位' },
        { id: 2, global_name: '站台位' }
      ],
      rack_list: [],
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    this.getRack()
  },
  mounted() {
  },
  methods: {
    async getRack(val) {
      if (val) {
        try {
          const data = await rackInfo('get', null, { params: { all: 1 }})
          this.rack_list = data || []
        } catch (e) {
        //
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await cacheLocations('get', null, { params: this.getParams })
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
    onSubmit() {
      this.$confirm('此操作将同步位置点是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.btnExportLoad1 = true
        syncLocations('get', null, {})
          .then(response => {
            this.btnExportLoad1 = false
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.getList()
          })
          .catch(response => {
            this.btnExportLoad1 = false
          })
      })
    },
    addFun() {
      this.dialogVisible = true
      this.currentObj.location_type = this.type_list.find(d => d.global_name === '缓存位') ? this.type_list.find(d => d.global_name === '缓存位').id : this.type_list[0].id
    },
    editShow(row, val) {
      if (val) {
        this.currentObj = Object.assign({}, row)
        this.dialogVisible = true
      } else {
        this.currentObj = Object.assign({}, row)
        this.dialogVisible1 = true
        this.getRack(true)
      }
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
      this.currentObj = { location_type: null }
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleClose1(done) {
      this.dialogVisible1 = false
      this.currentObj = { location_type: null }
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
        cacheLocationsDel('post', null, { data: { obj_ids: arr }})
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
        this.$store.dispatch('settings/operateTypeSetting', val)
        cacheLocationsUpdate('post', null, { data: { 'obj_ids': arr }})
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
            await cacheLocations(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            if (val) {
              this.handleClose(null)
            } else {
              this.handleClose1(null)
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
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = cacheLocations
      this.$store.dispatch('settings/operateTypeSetting', '导出')
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

