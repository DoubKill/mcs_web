<template>
  <div>
    <!-- 设备组设置 -->
    <el-form :inline="true" class="top-search-box">
      <!-- <el-form-item label="设备组名称"> -->
      <!-- <el-select
          v-model="getParams.group_name"
          clearable
          size="small"
          placeholder="请选择"
          filterable
          @visible-change="visibleChange"
          @change="changeList"
        >
          <el-option
            v-for="item in device_group_list"
            :key="item.global_name"
            :label="item.global_name"
            :value="item.id"
          />
        </el-select> -->
      <!-- </el-form-item> -->
      <el-form-item label="设备组类别">
        <el-select v-model="getParams.group_type" clearable size="small" placeholder="请选择" filterable @change="changeList">
          <el-option v-for="item in group_type_list" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
      </el-form-item>
    </el-form>
    <div v-loading="loading" class="center-box" style="margin-bottom: 44px;">
      <el-table ref="multipleTable" :data="tableData" style="width: 100%" stripe @selection-change="handleSelectionChange" @sort-change="arraySpanMethod">
        <!-- <el-table-column
          type="selection"
          width="40"
        /> -->
        <el-table-column label="设备组ID" prop="group_ID" sortable="custom">
          <el-table-column min-width="10" show-overflow-tooltip>
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.group_ID" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{row.group_ID}}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="设备组名称" prop="group_name" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.group_name" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.group_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="设备组成员" prop="members">
          <el-table-column min-width="25" show-overflow-tooltip>
            <!-- <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.members" size="small" clearable @input="changeList" />
            </template> -->
            <template slot-scope="{row}">
              <span v-for="item in row.members" :key="item">{{ item }}&nbsp;&nbsp;</span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="预警最大值" prop="warning_maximum" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.warning_maximum" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.warning_maximum }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="预警最小值" prop="warning_minimum" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.warning_minimum" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.warning_minimum }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="最大值" prop="maximum" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.maximum" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.maximum }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="最小值" prop="minimum" sortable="custom">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input prefix-icon="el-icon-search" v-model="getParams.minimum" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.minimum }}
            </template>
          </el-table-column>
        </el-table-column>
        <!-- <el-table-column
          prop="priority"
          label="优先级"
          show-overflow-tooltip
          min-width="10"
        /> -->
        <el-table-column label="操作" width="80">
          <template slot-scope="{row}">
            <el-button v-permission="['dev_groups','change']" size="small" type="text" @click="editShow(row)">修改</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-footer id="footer">
        <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
      </el-footer>
    </div>

    <el-dialog :visible.sync="dialogVisible" width="500px" :before-close="handleClose" title="编辑">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="100px">
        <el-form-item label="预警最大值" prop="warning_maximum">
          <el-input-number v-model="currentObj.warning_maximum" size="small" />
        </el-form-item>
        <el-form-item label="预警最小值" prop="warning_minimum">
          <el-input-number v-model="currentObj.warning_minimum" size="small" />
        </el-form-item>
        <el-form-item label="最大值" prop="maximum">
          <el-input-number v-model="currentObj.maximum" size="small" />
        </el-form-item>
        <el-form-item label="最小值" prop="minimum">
          <el-input-number v-model="currentObj.minimum" size="small" />
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
import page from '@/components/page'
import { platformGroup } from '@/api/base_w'
import common from '@/utils/common'
export default {
  name: 'DeviceGroupSettings',
  components: { page },
  data() {
    return {
      getParams: {},
      device_group_list: [],
      tableData: [{}],
      loading: false,
      dialogVisible: false,
      currentObj: {},
      rules: {
        maximum: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        minimum: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        warning_maximum: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        warning_minimum: [
          { required: true, message: '请填写', trigger: 'blur' }
        ]
      },
      btnLoading: false,
      total: 0,
      group_type_list: [{ name: '站台组', id: 1 }, { name: '堆栈组', id: 2 }]//{ name: '休息位组', id: 3 }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async arraySpanMethod(val) {
      try {
        let obj = { ordering: val.order === null ? null : (val.order === 'ascending' ? '' : '-') + (common.FOREIGN_KEY[val.prop] ? common.FOREIGN_KEY[val.prop] : val.prop) }
        Object.assign(this.getParams, obj)
        const data = await platformGroup('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
    },
    editShow(row) {
      this.dialogVisible = true
      this.currentObj = JSON.parse(JSON.stringify(row))
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleSelectionChange() { },
    visibleChange(bool) {
      if (bool) {
        this.getListAll()
      }
    },
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    async getList() {
      try {
        const data = await platformGroup('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
      } catch (e) {
        //
      }
    },
    async getListAll() {
      try {
        const data = await platformGroup('get', null, { params: { all: 1 } })
        this.device_group_list = data || []
      } catch (e) {
        //
      }
    },
    submitFun() {
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            await platformGroup('put', this.currentObj.id, { data: this.currentObj })
            this.$store.dispatch('settings/operateTypeSetting', '修改')
            this.$message.success('操作成功')
            this.btnLoading = false
            this.getList()
            this.handleClose(null)
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
