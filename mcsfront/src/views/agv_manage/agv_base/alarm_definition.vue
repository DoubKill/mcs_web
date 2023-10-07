<template>
  <div>
    <!-- 报警定义 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="报警名称">
          <el-input v-model="getParams.alarm_name" size="small" clearable placeholder="报警名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
        <el-button type="modify" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
        <el-button type="warning" icon="el-icon-connection" size="small" :loading="resetLoading" @click="resetFun">重置次数</el-button>
        <!-- <el-button type="danger" icon="el-icon-position" size="small" @click="synchroFun">同步后台</el-button> -->
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
          label="位信号"
          min-width="20"
        >
          <template slot-scope="scope">{{ scope.row.bit_signal }}</template>
        </el-table-column>
        <el-table-column
          prop="signal_num"
          label="编号"
          min-width="20"
        />
        <el-table-column
          prop="alarm_code"
          label="报警编号"
          min-width="20"
        />
        <el-table-column
          prop="alarm_name"
          label="报警名称"
          min-width="20"
        />
        <el-table-column
          prop="frequency"
          label="发生次数"
          min-width="20"
        />
        <el-table-column
          label="触发状态"
          min-width="20"
        >
          <template slot-scope="scope">
            <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.trigger_state?'':'info'">{{ scope.row.trigger_state?'是':'否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="occur_time"
          label="发生时间"
          min-width="20"
          show-overflow-tooltip
        />
        <el-table-column
          prop="release_time"
          label="解除时间"
          show-overflow-tooltip
          min-width="20"
        />
        <el-table-column
          prop="equip_no"
          label="机台号"
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
      width="500px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="位信号" prop="bit_signal">
          <el-input v-model="currentObj.bit_signal" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="编号" prop="signal_num">
          <el-input v-model="currentObj.signal_num" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="报警名称" prop="alarm_name">
          <el-input v-model="currentObj.alarm_name" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="报警编号" prop="alarm_code">
          <el-input v-model="currentObj.alarm_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="发生次数">
          <el-input-number v-model="currentObj.frequency" size="small" controls-position="right" :min="0" />
        </el-form-item>
        <el-form-item label="触发状态" prop="trigger_state">
          <el-select
            v-model="currentObj.trigger_state"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in [{name:'是',id:true},{name:'否',id:false}]"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="发生时间" prop="occur_time">
          <el-date-picker
            v-model="currentObj.occur_time"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            placeholder="选择日期"
          />
        </el-form-item>
        <el-form-item label="解除时间" prop="release_time">
          <el-date-picker
            v-model="currentObj.release_time"
            type="datetime"
            value-format="yyyy-MM-dd HH:mm:ss"
            placeholder="选择日期"
          />
        </el-form-item>
        <el-form-item label="机台号" prop="equip_no">
          <el-select
            v-model="currentObj.equip_no"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="item in device_list"
              :key="item.id"
              :label="item.equip_code"
              :value="item.equip_code"
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
import { alarmDefinitions, alarmDefinitionsDel, batchReset, basicsEquips } from '@/api/base_w'
import page from '@/components/page'
export default {
  name: 'AlarmDefinition',
  components: { page },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentObj: {},
      dialogVisible: false,
      rules: {
        bit_signal: [
          { required: true, message: '请填写位信号', trigger: 'blur' }
        ],
        signal_num: [
          { required: true, message: '请填写编号', trigger: 'blur' }
        ],
        alarm_code: [
          { required: true, message: '请填写报警编号', trigger: 'blur' }
        ],
        alarm_name: [
          { required: true, message: '请填写报警名称', trigger: 'blur' }
        ],
        trigger_state: [
          { required: true, message: '请填写触发状态', trigger: 'blur' }
        ],
        occur_time: [
          { required: true, message: '请选择发生时间', trigger: 'change' }
        ],
        release_time: [
          { required: true, message: '请选择解除时间', trigger: 'change' }
        ],
        equip_no: [
          { required: true, message: '请填写机台号', trigger: 'blur' }
        ]
      },
      currentVal: [],
      btnLoading: false,
      loading: true,
      exportLoading: false,
      resetLoading: false,
      device_list: []
    }
  },
  created() {
    this.getList()
    this.getOtherList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await alarmDefinitions('get', null, { params: this.getParams })
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
          basicsEquips('get', null, { params: { all: 1 }})
        ])
        this.device_list = a[0].filter(d => d.is_used)
      } catch (e) {
        //
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
    async resetFun() {
      if (!this.currentVal.length) {
        this.$message('请选择列表数据')
        return
      }
      const arr = []
      this.currentVal.forEach(d => {
        arr.push(d.id)
      })
      try {
        this.resetLoading = true
        await batchReset('post', null, { data: { obj_ids: arr }})
        this.resetLoading = false
        this.getList()
        this.$message.success('操作成功')
      } catch (e) {
        this.resetLoading = false
      }
    },
    async synchroFun() {
      try {
        await batchReset('post')
        this.$message.success('操作成功')
      } catch (e) {
        //
      }
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
        alarmDefinitionsDel('post', null, { data: { obj_ids: arr }})
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
            await alarmDefinitions(_api, this.currentObj.id || null, { data: this.currentObj })
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
      this.exportLoading = true
      const obj = Object.assign({ export: 1 }, this.getParams)
      const _api = alarmDefinitions
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

