<template>
  <div class="process-road">
    <!-- 工艺路线 未使用-->
    <div v-loading="loading">
      <div v-for="(item,index) in topCardData" :key="index" class="topCard">
        <div class="topOne">{{ item }}</div>
        <div class="bottomOne">上</div>
        <div class="bottomTwo">下</div>
      </div>
      <div>
        <div style="flex: 1;">
          <!-- <el-divider style="margin-left:20px;display: table;" content-position="left">阿里云</el-divider> -->
          <div v-for="(item,key,index) in bottomCardData" :key="index" class="bottomCard">
            <div class="leftOne">
              <div
                v-for="(item1,index1) in item.top"
                :key="index1"
                :style="{'background-image': 'linear-gradient(to right,'+
                  (item1.color.includes(',')?item1.color:(item1.color+','+item1.color))+')'}"
                class="smallBox"
                :title="item1.equip_no + key"
              >
                {{ item1.equip_no + key }}
              </div>
            </div>
            <div class="rightOne">
              <div
                v-for="(item1,index1) in item.bottom"
                :key="index1"
                :style="{'background-image': 'linear-gradient(to right,'+
                  (item1.color.includes(',')?item1.color:(item1.color+','+item1.color))+')'}"
                class="smallBox"
                :title="item1.equip_no + key"
                @click="clickRoad(item1.id)"
              >
                {{ item1.equip_no + key }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

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
                <el-radio v-for="item in process_list" :key="item.id" style="display: block;" :label="item.id" border disabled>{{ item.process_name }}</el-radio>
              </el-radio-group>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="box-card-dialog center">
            <div class="title-style">工序列表</div>
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
import { productionProcesses, craftManagements, basicsEquips } from '@/api/base_w'
import { viewPath } from '@/api/jqy'
import { Compact } from 'vue-color'
export default {
  name: 'ProcessRoad',
  components: { 'compact-picker': Compact },
  data() {
    return {
      tableData: [],
      total: 0,
      topCardData: [],
      bottomCardData: [],
      currentVal: [],
      btnLoading: false,
      loading: true,
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
      currentList: [],
      equip_list: [],
      w_index: '',
      process_list: []
      //
    }
  },
  created() {
    this.getList()
    this.getOtherList()
    // this.getProcessList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await viewPath('get', null, {})
        this.bottomCardData = data.data || []
        this.topCardData = data.processes || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async clickRoad(id) {
      try {
        const data = await craftManagements('get', id, { params: { }})

        this.currentObj = Object.assign({}, data)
        this.colors = this.currentObj.color
        this.dialogVisible = true
        this.clickRadio(this.currentObj.previous_process)
        if (this.currentObj.previous_process) {
          this.$set(this.currentObj, this.currentObj.previous_process, this.currentObj.previous_equips)
        }
        if (this.currentObj.back_process) {
          this.$set(this.currentObj, this.currentObj.back_process, this.currentObj.back_equips)
        }
      } catch (e) {
        //
      }
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
            this.btnLoading = false
            this.getList()
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    }
    // 弹框结束
  }
}
</script>

  <style lang="scss" scoped>
  .process-road{
    // display: flex;
    background: #F0F1F5;
    height: 90vh;
    overflow-x: auto;
    white-space: nowrap;
   .el-divider--horizontal{
      margin-left: 20px;
    }
   .topCard{
    color: #A0C9F1;
    display:inline-block;
    .topOne{
      border-radius: 0.3rem;
      background: #FFFFFF;
      margin-left: 20px;
      margin-right: 20px;
      text-align: center;
      margin-top: 20px;
      border-style:solid;
      border-color: #A0C9F1;
      border-width:1px;
      line-height: 40px;
      width: 160px;
      height: 40px;
    }
    .bottomOne{
      border-radius: 0.3rem;
      background: #FFFFFF;
      margin-left: 20px;
      text-align: center;
      line-height: 40px;
      margin-top: 10px;
      border-style:solid;
      border-color: #A0C9F1;
      border-width:1px;
      display:inline-block;
      width: 75px;
      height: 40px;
    }
  }
  .bottomTwo{
      border-radius: 0.3rem;
      background: #FFFFFF;
      margin-left: 10px;
      text-align: center;
      line-height: 40px;
      margin-top: 10px;
      border-style:solid;
      border-color: #A0C9F1;
      border-width:1px;
      display:inline-block;
      width: 75px;
      height: 40px;
    }
    .bottomCard{
      margin-left: 20px;
      margin-right: 20px;
      margin-top: 10px;
      float: left;
      .leftOne{
        width: 75px;
        min-height: 40px;
        float: left;
      }
      .rightOne{
        margin-left: 10px;
        min-height: 40px;
        width: 75px;
        float: left;
      }
      .smallBox{
        color: #FFFFFF;
        margin-top: 10px;
        border-radius: 0.3rem;
        text-align: center;
        border-style:solid;
        border-color: #A0C9F1;
        border-width:1px;
        line-height: 40px;
        width: 75px;
        height: 40px;
      }
    }
}

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

