<template>
  <div>
    <!-- 定线设置 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="分区">
          <el-input v-model="getParams.process_name" size="small" clearable placeholder="分区" />
        </el-form-item>
        <el-form-item>
          <el-radio-group v-model="getParams.device_type_name" size="small" @change="changeList">
            <el-radio-button v-for="item in deviceTypeList" :key="item.id" :label="item.type_name" />
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <!-- <el-button type="blue" icon="el-icon-plus" size="small" @click="editFun">编辑</el-button> -->
        <el-button type="danger" icon="el-icon-delete" size="small" @click="cancelFun">取消</el-button>
        <el-button type="modify" icon="el-icon-position" size="small" @click="submitFun">提交</el-button>
        <el-button type="blue" icon="el-icon-download" size="small" @click="exportFun">导出</el-button>
        <el-button type="warning" icon="el-icon-connection" size="small" @click="viewFun">日志查看</el-button>
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
          label="机台名称"
          width="120"
        >
          <template slot-scope="scope">{{ scope.row.device_name }}</template>
        </el-table-column>
        <el-table-column
          label="进料类别"
          width="100"
        >
          <template slot-scope="scope">
            <el-input-number v-model="scope.row.input_type" :disabled="!scope.row._isEdit" size="small" controls-position="right" :min="0" style="width:85px" />
          </template>
        </el-table-column>
        <el-table-column
          label="出料类别"
          width="100"
        >
          <template slot-scope="scope">
            <el-input-number v-model="scope.row.output_type" :disabled="!scope.row._isEdit" size="small" controls-position="right" :min="0" style="width:85px" />
          </template>
        </el-table-column>
        <el-table-column
          label="目标机台"
          width="100"
        >
          <template slot-scope="scope">
            <el-select
              v-model="scope.row.target_equip_line"
              clearable
              size="small"
              :disabled="!scope.row._isEdit"
            >
              <el-option
                v-for="item in scope.row.device_type_lines"
                :key="item.id"
                :label="item.line_code"
                :value="item.line_code"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column
          label="目标去向"
          width="80"
        >
          <template slot-scope="scope">{{ scope.row.destination }}</template>
        </el-table-column>
        <el-table-column
          label="定线"
        >
          <template slot-scope="scope">
            <el-checkbox-group v-model="scope.row.setting_lines" size="mini" class="readonlyFa">
              <el-checkbox-button v-for="city in scope.row.device_type_lines" :key="city.id" :label="city.id">{{ city.line_code }}</el-checkbox-button>
              <div v-if="!scope.row._isEdit" class="readonlyD" />
            </el-checkbox-group>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="50">
          <template slot-scope="{row}">
            <el-button size="small" type="text" @click="editFun(row)">修改</el-button>
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
  </div>
</template>

<script lang="js">
import { deviceTypes, lineInfos, setLines } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'AlignmentSetting',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: { device_type_name: '全部' },
      currentObj: {},
      dialogVisible: false,
      rules: {
        process_code: [
          { required: true, message: '请填写工序编号', trigger: 'blur' }
        ],
        process_name: [
          { required: true, message: '请填写工序名称', trigger: 'blur' }
        ],
        ordering: [
          { required: true, message: '请填写排序', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      deviceTypeList: [],
      bool: false
    }
  },
  created() {
    this.getList()
    this.getDeviceTypeList()
  },
  mounted() {
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const obj = Object.assign({}, this.getParams)
        if (obj.device_type_name === '全部') {
          obj.device_type_name = ''
        }
        const data = await lineInfos('get', null, { params: obj })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getDeviceTypeList() {
      try {
        const data = await deviceTypes('get', null, { params: { all: 1 }})
        this.deviceTypeList = data
        this.deviceTypeList.unshift({ id: '', type_name: '全部' })
      } catch (e) {
        //
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    synchroFun() {},
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    onReadonly() {

    },
    editFun(row) {
      if (this.bool) {
        this.bool = false
        this.getList()
      } else {
        this.bool = true
      }
      this.tableData.forEach(d => {
        if (row.id === d.id) {
          d._isEdit = true
        } else {
          d._isEdit = false
        }
      })
      this.tableData.splice(0, 0)
    },
    async cancelFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      try {
        this.currentVal.forEach(d => {
          d.setting_lines = []
        })
        this.btnLoading = true
        const _api = 'post'
        await setLines(_api, null, { data: this.currentVal })
        this.$message.success('操作成功')
        this.changeList()
        this.btnLoading = false
      } catch (e) {
        this.btnLoading = false
      }
    },
    viewFun() {
    },
    async submitFun() {
      const arr = this.tableData.filter(d => d._isEdit)
      if (!arr.length) {
        this.$message('暂无修改数据')
        return
      }
      try {
        this.btnLoading = true
        const _api = 'post'
        await setLines(_api, null, { data: arr })
        this.$message.success('操作成功')
        this.changeList()
        this.btnLoading = false
      } catch (e) {
        this.btnLoading = false
      }
    },
    exportFun() {
      this.btnExportLoad = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      if (obj.device_type_name === '全部') {
        obj.device_type_name = ''
      }
      const _api = lineInfos
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
.readonlyFa{
  position: relative;
}
.readonlyD{
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
}
</style>

