<template>
  <div>
    <!-- 工艺管理 未使用-->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="工艺编号">
          <el-input v-model="getParams.process_code" size="small" clearable placeholder="请输入工艺编号" />
        </el-form-item>
        <!-- <el-form-item label="工艺来源">
          <el-input v-model="getParams.vehicle_name" size="small" clearable placeholder="工艺来源" />
        </el-form-item>
        <el-form-item label="工序循环">
          <el-input v-model="getParams.vehicle_flag" size="small" clearable placeholder="工序循环" />
        </el-form-item> -->
        <el-form-item label="起始工序">
          <el-select
            v-model="getParams.previous_process_id"
            clearable
            size="small"
            placeholder="请选择"
            style="width:120px"
          >
            <el-option
              v-for="item in process_list"
              :key="item.process_name"
              :label="item.process_name"
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
          <el-button type="success" icon="el-icon-search" size="small" @click="changeList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="warning" icon="el-icon-turn-off" size="small" @click="useFun('禁用',1)">禁用</el-button>
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
          prop="craft_code"
          label="工艺编码"
          min-width="20"
        />
        <el-table-column
          prop="craft_desc"
          label="工艺描述"
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
        <el-table-column
          prop="created_time"
          label="创建时间"
          min-width="20"
        />
        <el-table-column
          prop="last_updated_time"
          label="更新时间"
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

    <!-- 弹框 -->
    <el-dialog
      :title="(currentObj.id?'编辑':'新建')+'工艺'"
      :visible.sync="dialogVisible"
      width="950px"
      :before-close="handleClose"
      class="dialog-style"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="80px" inline>
        <el-form-item label="颜色">
          <compact-picker v-model="colors" />
        </el-form-item>
        <br>
        <el-form-item label="工艺编码" prop="craft_code">
          <el-input v-model="currentObj.craft_code" size="small" :disabled="currentObj.id?true:false" />
        </el-form-item>
        <el-form-item label="工艺描述" prop="craft_desc">
          <el-input v-model="currentObj.craft_desc" size="small" />
        </el-form-item>
        <el-form-item label="内部循环" prop="is_internal_recycle">
          <el-radio-group v-model="currentObj.is_internal_recycle" size="medium">
            <el-radio-button :label="true">是</el-radio-button>
            <el-radio-button :label="false">否</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <el-row :gutter="12" class="center-box">
        <el-col :span="5">
          <div class="box-card-dialog">
            <div class="title-style one">工序库</div>
            <div class="checkbox-style">
              <el-radio-group v-model="currentObj.previous_process" size="small" @input="clickRadio">
                <el-radio v-for="(item, _i) in process_list" :key="item.id" :label="item.id" border :disabled="process_list&&(process_list.length===(_i+1))">{{ item.process_name }}</el-radio>
              </el-radio-group>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="box-card-dialog center">
            <div class="title-style">工序列表</div>
            <!-- <div>
              <div class="title-style one center-style">
                <span class="center-order-style">1</span> 工序列表
              </div>
            </div> -->
            <el-table
              ref="singleTable"
              :data="currentList"
              highlight-current-row
              style="width: 100%"
              :show-header="false"
              @current-change="handleCurrentChange"
            >
              <el-table-column
                label=""
              >
                <template slot-scope="{row,$index}">
                  <span class="center-order-style">{{ $index+1 }}</span>
                  <!-- <el-select v-if="['ALD', '正膜','背膜'].includes(currentList[0].process_name)&&$index===1" v-model="row.process_name" placeholder="请选择" size="small" @change="changeOperationList">
                    <el-option
                      v-for="(item,_key) in option"
                      :key="_key+$index"
                      :label="item"
                      :value="item"
                    />
                  </el-select> -->
                  <span>{{ row.process_name }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="11">
          <div class="box-card-dialog box-card-dialog-right">
            <div class="title-style">工序设备</div>
            <div style="padding-left:10px">
              <el-checkbox-group v-model="currentObj[w_index]" size="small" @input="clickCheckboxGroup">
                <el-checkbox v-for="(item) in equip_list" :key="item.id" :label="item.id" border>
                  {{ item.equip_code }}
                </el-checkbox>
              </el-checkbox-group>
            </div>
          </div>
        </el-col>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 弹框 -->
  </div>
</template>

<script>
import { productionProcesses, craftManagements, craftManagementsUpdate, craftManagementsDel, basicsEquips } from '@/api/base_w'
import page from '@/components/page'
import { Compact } from 'vue-color'
export default {
  name: 'ProcessManage',
  components: { page, 'compact-picker': Compact },
  data() {
    return {
      tableData: [],
      total: 0,
      getParams: {},
      currentVal: [],
      btnLoading: false,
      loading: true,
      currentOperationIndex: null,
      option: [],
      // 弹框需要
      dialogVisible: false,
      currentObj: {},
      colors: '#4D4D4D',
      rules: {
        craft_code: [
          { required: true, message: '请填写工艺编码', trigger: 'blur' }
        ],
        craft_desc: [
          { required: true, message: '请填写工艺描述', trigger: 'blur' }
        ],
        is_internal_recycle: [
          { required: true, message: '是否内部循环', trigger: 'change' }
        ]
      },
      process_list: [],
      currentList: [],
      equip_list: [],
      w_index: null
      //
    }
  },
  created() {
    this.getList()
    this.getOtherList()
  },
  mounted() {
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await craftManagements('get', null, { params: this.getParams })
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
      this.colors = '#4D4D4D'
      this.$set(this.currentObj, 'is_internal_recycle', true)
    },
    // 弹框需要
    async getOtherList() {
      try {
        const a = await Promise.all([
          productionProcesses('get', null, { params: { all: 1, is_used: true }})
        ])
        this.process_list = a[0] || []
      } catch (e) {
        //
      }
    },
    async getEquipList(id) {
      try {
        this.w_index = id
        if (!id) return
        if (!this.currentObj[id]) {
          this.$set(this.currentObj, id, [])
        }
        const a = await basicsEquips('get', null, { params: { all: 1, process: id }})
        this.equip_list = a.filter(d => d.is_used)
      } catch (e) {
        //
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.$refs.singleTable.setCurrentRow()
      this.currentList = []
      this.equip_list = []
      setTimeout(d => {
        this.$refs.ruleForm.resetFields()
        this.currentObj = {}
      }, 300)
      if (done) {
        done()
      }
    },
    clickRadio(val) {
      const obj = {}
      for (const key in this.currentObj) {
        if (Object.hasOwnProperty.call(this.currentObj, key)) {
          const element = this.currentObj[key]
          if (isNaN(key)) {
            obj[key] = element
          }
        }
      }
      this.currentObj = obj
      const _i = this.process_list.findIndex(d => d.id === val)
      if (this.$refs.singleTable) {
        this.$refs.singleTable.setCurrentRow()
      }
      this.equip_list = []
      this.currentList = []
      this.currentList.push(this.process_list[_i])
      // if (this.currentObj.id) {
      //   // 编辑进来的 查找一下后道工序
      //   const obj1 = this.process_list.find(d => this.currentObj.back_process === d.id)
      //   this.currentList.push(obj1)
      // } else {
      this.currentList.push(this.process_list[_i + 1])
      // }
      this.currentList = JSON.parse(JSON.stringify(this.currentList))
      if (this.process_list[_i].process_name === 'ALD') {
        this.option = ['正膜', '背膜']
      }
      if (['正膜', '背膜'].includes(this.process_list[_i].process_name)) {
        this.option = ['正膜', '背膜', '丝网']
      }
    },
    handleCurrentChange(val) {
      if (!val) return
      this.currentOperationIndex = this.currentList.findIndex(d => d.id === val.id)
      this.getEquipList(val ? val.id : '')
    },
    editShow(row) {
      this.currentObj = Object.assign({}, row)
      this.colors = this.currentObj.color
      this.dialogVisible = true
      this.clickRadio(this.currentObj.previous_process)
      if (this.currentObj.previous_process) {
        this.$set(this.currentObj, this.currentObj.previous_process, this.currentObj.previous_equips)
      }
      if (this.currentObj.back_process) {
        this.$set(this.currentObj, this.currentObj.back_process, this.currentObj.back_equips)
      }
    },
    clickCheckboxGroup() {
      this.currentObj.previous_process = this.currentList[0] ? this.currentList[0].id : ''
      this.currentObj.back_process = this.currentList[1] ? this.currentList[1].id : ''
      let previousName = ''
      let str1 = ''
      let backName = ''
      let str2 = ''
      if (this.currentObj.previous_process) {
        this.currentObj.previous_equips = this.currentObj[this.currentObj.previous_process]

        // 如果有前道工序 获取前道工序的 名字
        previousName = this.currentList.find(d => d.id === this.currentObj.previous_process).process_name
        const previousEquipsList = []
        this.equip_list.forEach((d, _ii) => {
          if (this.currentObj.previous_equips && this.currentObj.previous_equips.findIndex(dd => dd === d.id) > -1) {
            previousEquipsList[_ii] = d
            previousEquipsList[_ii].checkbox = true
          } else {
            previousEquipsList[_ii] = d
            previousEquipsList[_ii].checkbox = false
          }
        })
        for (let ii = 0; ii < previousEquipsList.length; ii++) {
          const element = previousEquipsList[ii]
          if (!str1 && element.checkbox) {
            str1 += (ii + 1)
          } else if ((previousEquipsList[ii].checkbox) && ((!previousEquipsList[ii + 1] || !previousEquipsList[ii + 1].checkbox) && (!previousEquipsList[ii - 1] || !previousEquipsList[ii - 1].checkbox))) {
            str1 += '.' + (ii + 1)
            continue
          } else if (previousEquipsList[ii].checkbox && (previousEquipsList[ii - 1] && previousEquipsList[ii - 1].checkbox) && (!previousEquipsList[ii + 1] || !previousEquipsList[ii + 1].checkbox)) {
            str1 += '-' + (ii + 1)
            continue
          } else if (previousEquipsList[ii].checkbox && ((!previousEquipsList[ii - 1] || !previousEquipsList[ii - 1].checkbox) && (previousEquipsList[ii + 1] && previousEquipsList[ii + 1].checkbox))) {
            str1 += '.' + (ii + 1)
            continue
          }
        }
      }
      if (this.currentObj.back_process) {
        this.currentObj.back_equips = this.currentObj[this.currentObj.back_process]

        // 如果有后道工序 获取后道工序的 名字
        backName = this.currentList.find(d => d.id === this.currentObj.back_process).process_name
        const backEquipsList = []
        this.equip_list.forEach((d, _ii) => {
          if (this.currentObj.back_equips && this.currentObj.back_equips.findIndex(dd => dd === d.id) > -1) {
            backEquipsList[_ii] = d
            backEquipsList[_ii].checkbox = true
          } else {
            backEquipsList[_ii] = d
            backEquipsList[_ii].checkbox = false
          }
        })
        for (let ii = 0; ii < backEquipsList.length; ii++) {
          const element = backEquipsList[ii]
          if (!str2 && element.checkbox) {
            str2 += (ii + 1)
          } else if ((backEquipsList[ii].checkbox) && ((!backEquipsList[ii + 1] || !backEquipsList[ii + 1].checkbox) && (!backEquipsList[ii - 1] || !backEquipsList[ii - 1].checkbox))) {
            str2 += '.' + (ii + 1)
            continue
          } else if (backEquipsList[ii].checkbox && (backEquipsList[ii - 1] && backEquipsList[ii - 1].checkbox) && (!backEquipsList[ii + 1] || !backEquipsList[ii + 1].checkbox)) {
            str2 += '-' + (ii + 1)
            continue
          } else if (backEquipsList[ii].checkbox && ((!backEquipsList[ii - 1] || !backEquipsList[ii - 1].checkbox) && (backEquipsList[ii + 1] && backEquipsList[ii + 1].checkbox))) {
            str2 += '.' + (ii + 1)
            continue
          }
        }
      }
      if (this.currentObj.craft_desc) {
        const craft_desc = this.currentObj.craft_desc.split('/')
        if (str1) {
          this.currentObj.craft_desc = [previousName + str1, craft_desc[1]].join('/')
        }
        if (str2) {
          this.currentObj.craft_desc = [craft_desc[0], backName + str2].join('/')
        }
      } else {
        this.currentObj.craft_desc = previousName + str1 + '/' + backName + str2
      }
    },
    submitFun() {
      if (!this.currentObj.id) {
        this.currentObj.color = this.colors.hex ? this.colors.hex : '#4D4D4D'
      } else {
        this.currentObj.color = this.colors.hex ? this.colors.hex : this.currentObj.color
      }
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            if (!this.currentList.length) {
              this.$message('请选择工序')
              return
            }
            if (this.currentObj.previous_process) {
              if (!this.currentObj[this.currentObj.previous_process] || !this.currentObj[this.currentObj.previous_process].length) {
                this.$message('请选择前工序设备')
                return
              }
            }
            if (this.currentObj.back_process) {
              if (!this.currentObj[this.currentObj.back_process] || !this.currentObj[this.currentObj.back_process].length) {
                this.$message('请选择后工序设备')
                return
              }
            }
            if (this.currentObj.previous_process === this.currentObj.back_process) {
              this.$message('工序列表不可相同')
              return
            }
            this.btnLoading = true
            const _api = this.currentObj.id ? 'put' : 'post'
            await craftManagements(_api, this.currentObj.id || null, { data: this.currentObj })
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
    // 弹框结束
    changeList() {
      this.getParams.page = 1
      this.getList()
    },
    currentChange(page, pageSize) {
      this.getParams.page = page
      this.getParams.page_size = pageSize
      this.getList()
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
        craftManagementsDel('post', null, { data: { obj_ids: arr }})
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
        craftManagementsUpdate('post', null, { data: { 'obj_ids': arr }})
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
    changeOperationList(val) {
      const obj = this.process_list.find(d => val === d.process_name)
      this.currentList[1].id = obj.id
      this.currentObj[this.currentObj.back_process] = []
      this.equip_list = []
      if (this.$refs.singleTable) {
        this.$refs.singleTable.setCurrentRow()
      }
      if (!obj) {
        this.$message('请去设备管理配置：正膜/背膜/丝网')
      }
    }
  }
}
</script>

  <style lang="scss" scoped>
    .box-card-dialog{
        border: 1px solid #DCDFE6;
        border-top:none;
        width: 100%;
        .el-checkbox{
            margin-right: 0;
        }
    }
    .title-style{
        height: 40px;
        line-height: 40px;
        background: #212b3f;
        color: #fff;
        padding-left:10px;
    }
    .one{
        background: rgb(188, 208, 225);
        color: rgb(84, 143, 192);
    }
    .center-style{
        padding-left: 16px;
        color:#68696d;
    }
    .center-order-style{
        display: inline-block;
        text-align: center;
        width: 16px;
        height: 15px;
        line-height: 13px;
        border: 1px solid #68696d;
        border-radius: 50%;
        background: #fff;
        margin-left: 10px;
        margin-right: 10px;
    }
    .checkbox-style{
        .el-radio.is-bordered+.el-radio.is-bordered{
            margin-left: 0px !important;
        }
        .el-radio.is-bordered{
            border: none !important;
        }
        max-height: 300px;
        overflow-y: scroll;
        overflow-x: hidden;

        &::-webkit-scrollbar {/*滚动条整体样式*/
            width:4px;/*高宽分别对应横竖滚动条的尺寸*/
            height:4px;
        }
        &::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
            border-radius:5px;
            -webkit-box-shadow: inset005pxrgba(0,0,0,0.2);
            background:rgba(0,0,0,0.2);
        }
    }
    .box-card-dialog-right{
        .el-checkbox.is-bordered+.el-checkbox.is-bordered{
          margin-top: 10px;
        }
    }
    .checkbox-style .el-radio.is-bordered{
        width: 100%;
        margin-right: 0;
    }

  </style>

