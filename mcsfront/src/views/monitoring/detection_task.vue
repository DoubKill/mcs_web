<template>
  <div>
    <!-- 检测任务配置 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <div class="botton-box">
        <el-button v-permission="['env_task','add']" type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button v-permission="['env_task','delete']" type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
      </div>
      <el-table ref="multipleTable" :data="tableData" stripe style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="40" />
        <el-table-column label="检测任务编号" prop="task_no">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.task_no" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.task_no }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="检测任务名称" prop="task_name">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.task_name" prefix-icon="el-icon-search" size="small" clearable @input="changeList" />
            </template>
            <template slot-scope="{row}">
              {{ row.task_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="所属工作区" prop="working_area">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.working_area" size="small" placeholder="" clearable @change="changeList" @visible-change="getOtherList">
                <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="{row}">
              {{ row.working_area_name }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="任务触发方式" prop="task_trigger_type">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.task_trigger_type" size="small" clearable placeholder="" @change="changeList">
                <el-option v-for="item in [{name:'单次',id:1},{name:'每日',id:2}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              {{ scope.row.task_trigger_type===1?'单次':'每日' }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="触发时间" prop="trigger_time">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <!-- <el-date-picker v-model="getParams.trigger_time" size="small" value-format="yyyy-MM-dd" type="date" placeholder="" @change="changeList" /> -->
            </template>
            <template slot-scope="{row}">
              {{ row.trigger_time }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="检测点列表" prop="envtasklocationrelation_set">
          <el-table-column min-width="10">
            <template slot-scope="scope">
              <!-- <el-select v-model="getParams.is_used" size="small" placeholder="">
                <el-option v-for="item in [{name:'是',id:true},{name:'否',id:false}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select> -->
            </template>
            <template slot-scope="{row}">
              <span v-for="item in row.envtasklocationrelation_set">
                {{ item.location_name }};
              </span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="启用标志" prop="is_used">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-select v-model="getParams.is_used" size="small" clearable placeholder="" @change="changeList">
                <el-option v-for="item in [{name:'是',id:true},{name:'否',id:false}]" :key="item.name" :label="item.name" :value="item.id" />
              </el-select>
            </template>
            <template slot-scope="scope">
              <el-tag size="mini" style="border-radius: 20px" effect="dark" :type="scope.row.is_used?'success':'info'">{{ scope.row.is_used?'是':'否' }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template slot-scope="{row}">
            <el-button v-permission="['env_task','change']" size="small" type="text" @click="editShow(row)">编辑</el-button>
            <el-button v-permission="['env_task','change']" size="small" type="text" @click="executeFun(row)">执行</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-footer id="footer">
        <page :old-page="false" :total="total" :current-page="getParams.page" @currentChange="currentChange" />
      </el-footer>
    </div>
    <el-dialog :title="(currentObj.id?'编辑':'新建')+'检测点'" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="检测任务编号" prop="task_no">
          <el-input :disabled="!!currentObj.id" v-model="currentObj.task_no" size="small" />
        </el-form-item>
        <el-form-item label="检测任务名称" prop="task_name">
          <el-input :disabled="!!currentObj.id" v-model="currentObj.task_name" size="small" />
        </el-form-item>
        <el-form-item label="所属工作区" prop="working_area">
          <el-select v-model="currentObj.working_area" size="small" placeholder="请选择" @change="clickWorkingArea">
            <el-option v-for="item in area_list" :key="item.id" :label="item.area_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务触发方式" prop="task_trigger_type">
          <el-select v-model="currentObj.task_trigger_type" size="small" placeholder="">
            <el-option v-for="item in [{name:'单次',id:1},{name:'每日',id:2}]" :key="item.name" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="触发时间" prop="bbb">
          <div v-if="currentObj.task_trigger_type===1">
            <el-date-picker v-model="currentObj._trigger_time" type="datetime" placeholder="选择日期时间" format="yyyy-MM-dd HH:mm" value-format="yyyy-MM-dd HH:mm" :clearable="false">
            </el-date-picker>
          </div>
          <div v-else>
            <span v-for="(item,key) in currentObj.list" :key="key">
              <el-time-picker v-model="item.name" placeholder="任意时间点" format="HH:mm" value-format="HH:mm" :clearable="false">
              </el-time-picker>
              <i v-if="currentObj.list.length!==key+1" style="font-size:25px;vertical-align: middle;cursor: pointer;" class="el-icon-remove" @click="clickDelFun(key)"></i>
            </span>
            <i style="font-size:25px;vertical-align: middle;cursor: pointer;" class="el-icon-circle-plus" @click="clickAddFun"></i>
          </div>
        </el-form-item>
        <el-form-item label="是否启用" prop="is_used">
          <el-select v-model="currentObj.is_used" size="small" placeholder="">
            <el-option v-for="item in [{name:'是',id:true},{name:'否',id:false}]" :key="item.name" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="检测点列表" prop="aaaa">
          <el-transfer draggable style="text-align: left; display: inline-block" v-model="currentObj.value4" :format="{
            noChecked: '${total}',
            hasChecked: '${checked}/${total}'
          }" :props="{
              key: 'id',
              label: 'location_name'
            }" @change="handleChange" :data="envCheck">
            <span slot-scope="{ option }">
              {{ option.location_name }}
              <i v-if="currentObj.value4&&currentObj.value4.findIndex(d=>d===option.id)>-1" style="font-size:25px;vertical-align: middle;cursor: pointer;" class="el-icon-caret-bottom" @click.prevent="clickBottomFun(option,false)"></i>
              <i v-if="currentObj.value4&&currentObj.value4.findIndex(d=>d===option.id)>-1" style="font-size:25px;vertical-align: middle;cursor: pointer;" class="el-icon-caret-top" @click.prevent="clickBottomFun(option,true)"></i>
            </span>
          </el-transfer>
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
import { issudTask, envCheckTasks, envCheckTasksDel, envCheckLocations, workAreas } from '@/api/base_w'
import draggable from 'vuedraggable'
import page from '@/components/page'
export default {
  name: 'DetectionTask',
  components: {
    draggable,
    page
  },
  data() {
    return {
      tableData: [],
      loading: false,
      dialogVisible: false,
      currentVal: [],
      currentObj: { list: [{ name: null }], is_used: true },
      area_list: [],
      rules: {
        task_no: [
          { required: true, message: '请填写检测任务编号', trigger: 'blur' }
        ],
        task_name: [
          { required: true, message: '请填写检测任务名称', trigger: 'blur' }
        ],
        working_area: [
          { required: true, message: '请选择所属工作区', trigger: 'change' }
        ],
        task_trigger_type: [
          { required: true, message: '请选择任务触发方式', trigger: 'change' }
        ]
      },
      btnLoading: false,
      getParams: {},
      total: 0,
      envCheck: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await envCheckTasks('get', null, { params: this.getParams })
        this.tableData = data.results || []
        this.total = data.count
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getEnvCheckList(id) {
      try {
        const data = await envCheckLocations('get', null, { params: { all: 1, working_area: id } })
        this.envCheck = data || []
        if (this.currentObj.value4 && this.currentObj.value4.length) {
          this.envCheck.forEach(item => {
            let sortId = this.currentObj.value4.indexOf(item.id)
            item.sortId = sortId
          })
          this.envCheck.sort(sort('sortId'))
        }
      } catch (e) {
        //
      }
    },
    clickWorkingArea(val) {
      if (val) {
        this.getEnvCheckList(val)
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = { list: [{}], is_used: true }
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    async getOtherList(val) {
      if (val) {
        try {
          const a = await workAreas('get', null, { params: { all: 1 } })
          this.area_list = a || []
        } catch (e) {
          //
        }
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.getOtherList(true)
      this.dialogVisible = true
    },
    editShow(row) {
      this.getOtherList(true)
      this.currentObj = Object.assign({}, row)
      this.$set(this.currentObj, 'value4', [])
      this.currentObj.envtasklocationrelation_set.forEach(d => {
        this.currentObj.value4.push(d.check_location)
      })
      this.getEnvCheckList(row.working_area)
      if (this.currentObj.task_trigger_type === 1) {
        this.$set(this.currentObj, '_trigger_time', this.currentObj.trigger_time[0])
      } else {
        this.$set(this.currentObj, 'list', [])
        this.currentObj.trigger_time.forEach(d => {
          this.currentObj.list.push({ name: d })
        })
      }
      this.dialogVisible = true
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
        envCheckTasksDel('post', null, { data: { obj_ids: arr } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', '删除')
            this.getList()
          }).catch(() => {
          })
      }).catch(() => {
      })
    },
    executeFun(row) {
      this.$confirm('此操作执行, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        issudTask('post', null, { data: { "task_id": row.id } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', '执行')
          }).catch(() => {
          })
      }).catch(() => {
      })
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
    clickAddFun() {
      this.currentObj.list.push({ name: null })
    },
    clickDelFun(index) {
      this.currentObj.list.splice(index, 1)
    },
    handleChange() {
      if (this.currentObj.value4 && this.currentObj.value4.length) {
        this.envCheck.forEach(item => {
          let sortId = this.currentObj.value4.indexOf(item.id)
          item.sortId = sortId
        })
        this.envCheck.sort(sort('sortId'))
      }
    },
    clickBottomFun(val, bool) {
      let _i = null, item
      _i = this.envCheck.findIndex(d => d.id === val.id)

      let a = bool ? this.envCheck[_i - 1] : this.envCheck[_i + 1]
      let _iBool = this.currentObj.value4.findIndex(d => d === (a && a.id))
      if (_iBool === -1) {
        return
      }

      item = this.envCheck[_i];
      if (bool) {
        this.envCheck[_i] = this.envCheck[_i - 1];
        this.envCheck[_i - 1] = item;
      } else {
        this.envCheck[_i] = this.envCheck[_i + 1];
        this.envCheck[_i + 1] = item;
      }
      this.$forceUpdate()
    },
    submitFun() {
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            if (this.currentObj.task_trigger_type === 1) {
              // 单次
              this.currentObj.trigger_time = [this.currentObj._trigger_time]
            } else {
              this.currentObj._trigger_time = null
              this.currentObj.trigger_time = []
              if (this.currentObj.list.length === 0) {
                this.$message('请选择触发时间')
                return
              }
              this.currentObj.list.forEach(d => {
                this.currentObj.trigger_time.push(d.name)
              })
            }
            if (!this.currentObj.value4 || this.currentObj.value4.length === 0) {
              this.$message('请选择检测点')
              return
            }
            this.currentObj.envtasklocationrelation_set = []
            this.envCheck.forEach((d, index) => {
              if (this.currentObj.value4.findIndex(D => D === d.id) > -1) {
                this.currentObj.envtasklocationrelation_set.push({
                  check_location: d.id,
                  ordering: this.currentObj.envtasklocationrelation_set.length
                })
              }
            })
            const _api = this.currentObj.id ? 'put' : 'post'
            this.btnLoading = true
            await envCheckTasks(_api, this.currentObj.id || null, { data: this.currentObj })
            this.$message.success('操作成功')
            this.handleClose(null)
            this.getList()
            this.btnLoading = false
            if (this.currentObj.id) {
              this.$store.dispatch('settings/operateTypeSetting', '变更')
            } else {
              this.$store.dispatch('settings/operateTypeSetting', '新增')
            }
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    changeId(val) {

    }
  }
}

function sort(prop) {
  return function(obj1, obj2) {
    var val1 = obj1[prop]
    var val2 = obj2[prop]
    if (!isNaN(Number(val1)) && !isNaN(Number(val2))) {
      val1 = Number(val1)
      val2 = Number(val2)
    }
    if (val1 < val2) {
      return -1
    } else if (val1 > val2) {
      return 1
    }
    else {
      return 0
    }
  }
}
  </script>
  
  <style lang="scss" scoped>
  
  </style>
  