<template>
  <div>
    <!-- 缓存位组管理 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="缓存位组编号">
          <el-input v-model="getParams.location_group_code" size="small" clearable placeholder="请输入缓存位组编号" />
        </el-form-item>
        <el-form-item label="类别">
          <el-select
            v-model="getParams.location_group_type"
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
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button v-permission="['cache_locations_group','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['cache_locations_group','export']" type="blue" icon="el-icon-download" size="small" :loading="btnExportLoad" @click="exportFun">导出</el-button>
        <el-button v-permission="['cache_locations_group','update']" type="danger" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
        <el-button v-permission="['cache_locations_group','update']" type="danger" icon="el-icon-open" size="small" @click="useFun('启用',1)">启用</el-button>
        <el-button v-permission="['cache_locations_group','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
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
          prop="location_group_code"
          label="缓存位组编号"
          min-width="20"
        />
        <el-table-column
          prop="location_group_name"
          label="缓存位组名称"
          min-width="20"
        />
        <el-table-column
          prop="location_group_type_name"
          label="类别"
          min-width="16"
        />
        <el-table-column
          label="启用标志"
          width="80"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'启用':'禁用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="choice_locations"
          label="已选择缓存位"
          min-width="30"
        />
        <el-table-column
          prop="created_username"
          label="创建人"
          show-overflow-tooltip
          min-width="15"
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
          min-width="15"
        />
        <el-table-column
          prop="last_updated_time"
          label="修改时间"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column label="操作" width="60">
          <template slot-scope="{row}">
            <el-button v-permission="['cache_locations_group','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
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
      :title="(currentObj.id?'编辑':'新建')+'缓存位组'"
      :visible.sync="dialogVisible"
      width="1300px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px" inline>
        <el-form-item label="缓存位组编号" prop="location_group_code">
          <el-input v-model="currentObj.location_group_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="缓存位组名称" prop="location_group_name">
          <el-input v-model="currentObj.location_group_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="类别" prop="location_group_type">
          <el-select
            v-model="currentObj.location_group_type"
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
        <el-form-item label="选择缓存位" style="" prop="locations">
          <el-transfer
            v-model="currentObj.locations"
            filterable
            :filter-method="filterMethod"
            :props="{
              key: 'id',
              label: 'location_code'
            }"
            :titles="['备选缓存位','已选缓存位']"
            :data="location_list"
          />
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
import { getGlobalCodes } from '@/api/basics'
import { cacheLocations, cacheLocationsGroup, cacheLocationsGroupUpdate, cacheLocationsGroupDel } from '@/api/jqy'
import page from '@/components/page'
export default {
  name: 'CacheGroupSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: { location_group_type: null, locations: [] },
      btnExportLoad: false,
      dialogVisible: false,
      rules: {
        location_group_code: [
          { required: true, message: '请填写缓存位组编号', trigger: 'blur' }
        ],
        location_group_name: [
          { required: true, message: '请填写缓存位组名称', trigger: 'blur' }
        ],
        location_group_type: [
          { required: true, message: '请填写类别', trigger: 'blur' }
        ]
      },
      district: null,
      location_list: [],
      type_list: [
        { id: 1, global_name: '专属缓存位组' },
        { id: 2, global_name: '公共缓存位组' },
        { id: 3, global_name: '接力缓存位组' },
        { id: 4, global_name: '决策缓存位组' }
      ],
      currentVal: [],
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getList()
    // this.getType()
  },
  mounted() {
  },
  methods: {
    filterMethod(query, item) {
      return item.location_code.indexOf(query) > -1
    },
    async getType() {
      try {
        const data = await getGlobalCodes({ all: 1, type_name: '缓存位组类别' })
        this.type_list = data || []
      } catch (e) {
        //
      }
    },
    async getLocations() {
      try {
        const data = await cacheLocations('get', null, { params: { all: 1, location_type: 1 }})
        this.location_list = data || []
        this.location_list.forEach(d => {
          d.disabled = !d.is_used
          if (!d.is_used) {
            d.location_code = d.location_code + ' 已禁用'
          }
        })
      } catch (e) {
        //
      }
    },
    // pickLocations() {
    //   if (this.currentObj.location_group_type) {
    //     if (this.type_list.find(d => d.id === this.currentObj.location_group_type).global_name === '机台专属') {
    //       const arr = []
    //       this.location_list.forEach(d => {
    //         arr.push(d.id)
    //       })
    //       this.$set(this.currentObj, 'locations', arr)
    //     } else {
    //       this.$set(this.currentObj, 'locations', [])
    //     }
    //   }
    // },
    async getList() {
      try {
        this.loading = true
        const data = await cacheLocationsGroup('get', null, { params: this.getParams })
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
      this.getLocations()
      this.dialogVisible = true
      this.district = null
      // this.currentObj.location_group_type = this.type_list.find(d => d.global_name === '机台专属').id
    },
    editShow(row) {
      this.getLocations()
      this.currentObj = Object.assign({}, row)
      this.district = null
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
      this.currentObj = { location_group_type: null, locations: [] }
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
        cacheLocationsGroupDel('post', null, { data: { obj_ids: arr }})
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
        cacheLocationsGroupUpdate('post', null, { data: { 'obj_ids': arr }})
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
    submitFun() {
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            if (this.currentObj.locations.length < 1) {
              this.$message('缓存位至少选择一个')
              return
            }
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
            await cacheLocationsGroup(_api, this.currentObj.id || null, { data: this.currentObj })
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
      const _api = cacheLocationsGroup
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

