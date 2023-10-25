<template>
  <div class="alignment_query">
    <!-- 定线管理 -->
    <el-tabs v-model="tabCurrent" class="w-tabs-style" @tab-click="handleClick">
      <el-tab-pane v-for="(item) in tabHearder" :key="item.id" :label="item.name" :name="item.id" />
    </el-tabs>
    <div class="top-search-box" v-if="tabCurrent==='2'">
      <el-button v-permission="['schemas','change']" type="primary" @click="addLine">新增</el-button>
    </div>
    <div class="center-box" style="white-space: nowrap;overflow: initial;">
      <ul v-if="newAlignmentNum.length>0" class="setBoxUl">
        <li v-for="itemHead in newAlignmentNum[0].process_plats" :key="itemHead.process_id" class="setBoxLi">{{ itemHead.process_name }}</li>
      </ul>
      <div v-for="(_item,_i) in newAlignmentNum" :key="_i" class="alignmentNumStyle">
        <div :class="['styleLeft']">
          <div @click="clickOperateMark" :class="[operateMark.length?'radioAfter':'']"></div>
          <div v-if="_i===newAlignmentNum.length-1&&tabCurrent==='2'">未定线</div>
          <el-radio v-else-if="tabCurrent==='2'" v-model="aaa" :label="_i" class="" @input="inputRadio">{{_item.route_ID}} ({{ _item.route_name }})</el-radio>
          <span v-else>{{_item.route_ID}} ({{ _item.route_name }})</span>
          <div v-permission="['schemas','change']" v-if="aaa === _i&&_i!==newAlignmentNum.length-1&&tabCurrent==='2'">
            <el-button class="setButtonStyle" type="primary" size="mini" v-loading="tableBtnLoading&&clickIndex===_i" :disabled="_item.is_forbidden&&!!_item.id" @click="useFun(_i,1)">暂存</el-button>
            <el-button :disabled="!_item.id||_item.is_forbidden||!_item.is_used" type="primary" size="mini" @click="disableFun(_i,4)">恢复</el-button>
            <el-button type="primary" size="mini" :disabled="_item.is_forbidden||!_item.id" @click="disableFun(_i,3,_item)">禁用</el-button>
            <el-button v-loading="tableBtnLoading&&clickIndex===_i" type="primary" :disabled="!_item.id" size="mini" @click="useFun(_i,2)">使用</el-button>
            <el-button type="primary" :disabled="!_item.id" size="mini" @click="deleteFun(_item.id,_item)">删除</el-button>
          </div>
        </div>
        <div v-for="(faItem,i) in _item.process_plats" :key="faItem.id" class="processPlatsStyle">
          <ul class="setCenterBoxUl scrollBar">
            <li v-for="(itemC,ii) in faItem.plt_devices" :key="itemC.dp_type+' '+itemC.instance_id+''+ii" :style="{'background':
                itemC.dp_type===1?'#f8d4e6':itemC.dp_type===2?'#bed5e9':''}" class="setCenterBoxLi" @dblclick="dblclickLi(ii,i,_i,itemC)">
              {{ itemC.instance_name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div v-if="newAlignmentNum.length===0" style="text-align:center">暂无数据</div>

    <el-dialog :visible.sync="dialogVisible" width="500px" :before-close="handleClose">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="定线ID" prop="route_ID">
          <el-input-number v-model="currentObj.route_ID" size="small" controls-position="right" />
        </el-form-item>
        <el-form-item label="定线名" prop="district_name">
          <el-input v-model="currentObj.district_name" size="small" />
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
import { routingSchema, currentRoute } from '@/api/base_w'
import draggable from 'vuedraggable'
export default {
  name: 'AlignmentQuery',
  components: {
    draggable
  },
  data() {
    return {
      tabCurrent: '1',
      tabHearder: [{ id: '1', name: '当前定线' }, { id: '2', name: '预定线' }], // 
      headList: 10,
      currentIndex: null,
      alignmentNum: [],
      newAlignmentNum: [],
      //   myArray: {
      //     route_name: '测试',
      //     process_plats: [{
      //       name: 88,
      //       id: 1,
      //       plt_devices: [1, 2, 3]
      //     },
      //     {
      //       name: 11,
      //       id: 2,
      //       plt_devices: [1, 2, 3]
      //     },
      //     {
      //       name: 22,
      //       id: 3
      //     },
      //     {
      //       name: 33,
      //       id: 4
      //     }
      //     ] },
      aaa: null,
      dialogVisible: false,
      currentObj: {},
      rules: {
        district_name: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        route_ID: [
          { required: true, message: '请填写', trigger: 'blur' }
        ]
      },
      btnLoading: false,
      clickIndex: null,
      tableBtnLoading: false,
      operateMark: []
    }
  },
  mounted() {
  },
  created() {
    this.getCurrentList()
  },
  methods: {
    async getList() {
      try {
        const data = await routingSchema('get', null, { params: {} })
        this.alignmentNum = data || []

        this.newAlignmentNum = JSON.parse(JSON.stringify(data)) || []
        this.reductionFun()
      } catch (e) {
        //
      }
    },
    async getCurrentList() {
      try {
        this.newAlignmentNum = []
        const data = await currentRoute('get', null, { params: {} })
        this.newAlignmentNum = data || []
      } catch (e) {
        //
      }
    },
    handleClick(val) {
      this.operateMark = []
      if (val.name === '1') {
        this.getCurrentList()
      } else {
        this.getList()
      }
    },
    dblclickLi(index, devicesIndex, faIndex, item) {
      if (this.aaa === null) {
        return
      }
      if (!(this.aaa === faIndex || this.newAlignmentNum.length - 1 === faIndex)) {
        return
      }

      // 记录是否有过修改
      if (!this.operateMark.length) {
        this.operateMark.push(item.instance_name + '' + item.pc_id)
      } else {
        let _ii = this.operateMark.findIndex(d => d === item.instance_name + '' + item.pc_id)
        console.log(_ii);
        if (_ii > -1) {
          this.operateMark.splice(_ii, 1)
        } else {
          this.operateMark.push(item.instance_name + '' + item.pc_id)
        }
      }

      this.newAlignmentNum[faIndex].process_plats[devicesIndex].plt_devices.splice(index, 1)
      let _index = this.aaa === faIndex ? this.newAlignmentNum.length - 1 : this.aaa
      if ((this.newAlignmentNum[_index].process_plats[devicesIndex].plt_devices).findIndex(d => d.instance_name === item.instance_name) === -1) {
        this.newAlignmentNum[_index].process_plats[devicesIndex].plt_devices.push(item)
      }
    },
    inputRadio() {
      this.operateMark = []

      this.reductionFun()
    },
    reductionFun() {
      if (this.aaa !== null) {
        let _current = this.alignmentNum[this.aaa]
        let _undetermined = this.alignmentNum[this.alignmentNum.length - 1]
        let _currentCopy = JSON.parse(JSON.stringify(_undetermined))
        for (const key in _undetermined) {
          if (Object.hasOwnProperty.call(_undetermined, key)) {
            _undetermined.process_plats.forEach((d, ii) => {
              let _arr = []
              d.plt_devices.forEach((dd, i) => {
                if (_current.process_plats[ii].plt_devices.length !== 0) {
                  let _index = _current.process_plats[ii].plt_devices.findIndex(ddd => ddd.instance_name === dd.instance_name && ddd.dp_type === dd.dp_type)
                  if (_index === -1) {
                    _arr.push(dd)
                  }
                } else {
                  _arr.push(dd)
                }
              })
              _currentCopy.process_plats[ii].plt_devices = _arr
            })
          }
        }
        this.newAlignmentNum[this.newAlignmentNum.length - 1] = _currentCopy
      }
    },
    clickOperateMark() {
      if (this.operateMark.length) {
        this.$message('当前定线正在操作,请先暂存或启用')
      }
    },
    disableFun(_i, type, _item) {
      this.useFun(_i, type)
    },
    startFun(e, i, faItem) {
      this.currentIndex = i
    },
    endFun(e, faI, i, _item) {
      // 同一条竖线的 去重
      const arr = this.newAlignmentNum[this.aaa] ? this.newAlignmentNum[this.aaa].process_plats[i].plt_devices : []
      const obj = {}
      const peon = arr.reduce((cur, next) => {
        obj[next.instance_name] ? '' : obj[next.instance_name] = true && cur.push(next)
        return cur
      }, [])
      if (this.newAlignmentNum[this.aaa]) {
        this.newAlignmentNum[this.aaa].process_plats[i].plt_devices = peon
      }

      const arr1 = this.newAlignmentNum[this.newAlignmentNum.length - 1].process_plats[i].plt_devices
      const obj1 = {}
      const peon1 = arr1.reduce((cur, next) => {
        obj1[next.instance_name] ? '' : obj1[next.instance_name] = true && cur.push(next)
        return cur
      }, [])
      this.newAlignmentNum[this.newAlignmentNum.length - 1].process_plats[i].plt_devices = peon1

      this.currentIndex = null
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    addLine() {
      this.dialogVisible = true
    },
    submitFun() {
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            this.dialogVisible = false
            this.btnLoading = false

            this.aaa = this.newAlignmentNum.length - 1
            const arr = { process_plats: [] }
            this.newAlignmentNum[0].process_plats.forEach((d, i) => {
              arr.process_plats.push({ plt_devices: [], process_id: d.process_id, process_name: d.process_name })
              arr.route_name = this.currentObj.district_name
              arr.route_ID = this.currentObj.route_ID
            })
            this.newAlignmentNum.splice(-1, 0, arr)
            this.handleClose(null)
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    async useFun(index, bool) {
      try {
        if (!this.newAlignmentNum[index].id && bool === 2) {
          // 新增需要先点击 暂存
          this.$message('新增需要先点击暂存')
          return
        }
        this.clickIndex = index
        this.tableBtnLoading = true
        const _api = this.newAlignmentNum[index].id ? 'put' : 'post'
        let _obj = this.newAlignmentNum[index]
        _obj.operation_type = bool
        let _str = bool === 1?'暂存':bool === 2?'使用':bool === 3?'禁用':'恢复'
        await routingSchema(_api, this.newAlignmentNum[index].id ? this.newAlignmentNum[index].id : null, { data: _obj })
        this.$store.dispatch('settings/operateTypeSetting', this.newAlignmentNum[index].id ? _str + _obj.route_name : '新增'+_obj.route_name)
        this.$message.success('保存成功')
        this.operateMark = []
        this.tableBtnLoading = false
        this.getList()
      } catch (e) {
        this.tableBtnLoading = false
      }
    },
    deleteFun(id, item) {
      if (!item.is_forbidden) {
        this.$message('请先点击禁用')
        return
      }
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (!id) {
          this.$message('请先点击使用')
          return
        }
        routingSchema('delete', id, { data: { id: id } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', '删除'+item.route_name)
            this.getList()
          }).catch(() => {
          })
      }).catch(() => {
      })
    }
  }
}
</script>

<style lang="scss">
.alignment_query{
    .setBoxUl{
        margin-left: 100px;
    }
    .setBoxLi{
      vertical-align: middle;
        display: inline-block;
        background: rgb(86,80,119);
        color:#fff;
        height: 45px;
        width: 80px;
        padding:5px 0;
        text-align: center;
        border: 1px solid #fff;
        white-space: normal;
    }
    .processPlatsStyle{
      display:inline-block;
    }
    .alignmentNumStyle{
      display:flex;
      margin-bottom:5px;
    }
    .setCenterBoxUl{
        width: 80px;
        text-align: center;
        float: left;
        height: 100%;
        border: 1px solid #bbb8b8;
        &::-webkit-scrollbar-track-piece {
            background: #d3dce6;
        }

        &::-webkit-scrollbar {
            width: 1px;
        }

        &::-webkit-scrollbar-thumb {
            background: #99a9bf;
            border-radius: 20px;
        }
    }
    .setCenterBoxLi{
        padding:5px 0;
        margin:4px 0;
        background: #bcffa5;
        white-space: normal;
        cursor: pointer;
    }
    .styleLeft{
        display: inline-block;
        overflow: hidden;
        position: relative;
        min-width: 100px;
        width: 100px;
        border: 1px solid rgb(187, 184, 184);
        padding:2px;
        padding-left:10px;
        padding-top:8px;
        font-weight: 700;
        white-space: normal;
        // text-align: center;
        button{
            margin-bottom:2px;
        }
        .el-radio__label{
          white-space: normal;
          word-break: break-all;
        }
        .el-radio{
          margin-right: 0;
        }
    }
    .el-radio__label{
        font-weight: 700 !important;
    }
    .setButtonStyle{
       margin-left:10px;
       margin-top:15px;
    }
    
    .w-tabs-style{
        margin-left:15px;
    }
    .radioAfter{
        position: absolute;
        display: inline-block;
        width:100%;
        height: 29px;
        z-index: 1;
    }
    .center-box{
      overflow-y: scroll !important;;
      height: 71vh;
    }
}
</style>
