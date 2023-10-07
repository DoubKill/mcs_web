<template>
  <div class="alignment_query">
    <!-- 定线管理 -->
    <div class="top-search-box">
      <el-button type="primary" @click="addLine">新增</el-button>
    </div>
    <div class="center-box" style="white-space: nowrap;overflow: auto;">
      <ul v-if="alignmentNum.length>0" class="setBoxUl">
        <li v-for="itemHead in alignmentNum[0].process_plats" :key="itemHead.process_id" class="setBoxLi">{{ itemHead.process_name }}</li>
      </ul>
      <div v-for="(_item,_i) in alignmentNum" :key="_i" class="alignmentNumStyle">
        <div class="styleLeft">
          <div v-if="_i===alignmentNum.length-1">未定线</div>
          <el-radio v-else v-model="aaa" :label="_i">{{ _item.route_name }}</el-radio>
          <div v-if="aaa === _i&&_i!==alignmentNum.length-1">
            <el-button v-loading="tableBtnLoading&&clickIndex===_i" type="primary" class="setButtonStyle" size="mini" @click="useFun(_i)">使用</el-button>
            <!-- <el-button type="primary" size="mini">使用</el-button>
            <el-button type="primary" size="mini">禁用</el-button>-->
            <el-button type="primary" size="mini" @click="deleteFun(_item.id)">删除</el-button>
          </div>
        </div>
        <div v-for="(faItem,i) in _item.process_plats" :key="faItem.id" class="processPlatsStyle">
          <ul class="setCenterBoxUl scrollBar">
            <draggable
              v-model="faItem.plt_devices"
              :disabled="(_i!==alignmentNum.length-1&&aaa !== _i)||(currentIndex!==null&&currentIndex!==i)"
              group="people"
              style="height:100%"
              @start="startFun($event,i)"
              @end="endFun($event,_i,i,_item)"
            >
              <li
                v-for="(itemC,ii) in faItem.plt_devices"
                :key="itemC.dp_type+' '+itemC.instance_id+''+ii"
                :style="{'background':_i===alignmentNum.length-1?'#eee':
                  itemC.dp_type===1?'#f8d4e6':itemC.dp_type===2?'#bed5e9':''}"
                class="setCenterBoxLi"
              >
                <!-- {{ itemC.hasOwnProperty('device_id')?itemC.device_desc:itemC.platform_desc }} -->
                {{ itemC.instance_name }}
              </li>
            </draggable>
          </ul>
        </div>
      </div>
    </div>
    <div v-if="alignmentNum.length===0" style="text-align:center">暂无数据</div>

    <el-dialog
      :visible.sync="dialogVisible"
      width="500px"
      :before-close="handleClose"
    >
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="新建线" prop="district_name">
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
import { routingSchema } from '@/api/base_w'
import draggable from 'vuedraggable'
export default {
  name: 'AlignmentQuery',
  components: {
    draggable
  },
  data() {
    return {
      headList: 10,
      currentIndex: null,
      alignmentNum: [],
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
        ]
      },
      btnLoading: false,
      clickIndex: null,
      tableBtnLoading: false
    }
  },
  mounted() {
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        const data = await routingSchema('get', null, { params: {}})
        this.alignmentNum = data || []
      } catch (e) {
        //
      }
    },
    startFun(e, i, faItem) {
      this.currentIndex = i
    },
    endFun(e, faI, i, _item) {
      // 同一条竖线的 去重
      const arr = this.alignmentNum[this.aaa] ? this.alignmentNum[this.aaa].process_plats[i].plt_devices : []
      const obj = {}
      const peon = arr.reduce((cur, next) => {
        obj[next.instance_name] ? '' : obj[next.instance_name] = true && cur.push(next)
        return cur
      }, [])
      if (this.alignmentNum[this.aaa]) {
        this.alignmentNum[this.aaa].process_plats[i].plt_devices = peon
      }

      const arr1 = this.alignmentNum[this.alignmentNum.length - 1].process_plats[i].plt_devices
      const obj1 = {}
      const peon1 = arr1.reduce((cur, next) => {
        obj1[next.instance_name] ? '' : obj1[next.instance_name] = true && cur.push(next)
        return cur
      }, [])
      this.alignmentNum[this.alignmentNum.length - 1].process_plats[i].plt_devices = peon1

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
      this.$refs.ruleForm.validate(async(valid) => {
        if (valid) {
          try {
            this.btnLoading = true
            this.dialogVisible = false
            this.btnLoading = false

            this.aaa = this.alignmentNum.length - 1
            const arr = { process_plats: [] }
            this.alignmentNum[0].process_plats.forEach((d, i) => {
              arr.process_plats.push({ plt_devices: [], process_id: d.process_id, process_name: d.process_name })
              arr.route_name = this.currentObj.district_name
            })
            this.alignmentNum.splice(-1, 0, arr)
            this.handleClose(null)
          } catch (e) {
            this.btnLoading = false
          }
        } else {
          return false
        }
      })
    },
    async useFun(index) {
      try {
        this.clickIndex = index
        this.tableBtnLoading = true
        const _api = this.alignmentNum[index].id ? 'put' : 'post'
        await routingSchema(_api, this.alignmentNum[index].id ? this.alignmentNum[index].id : null, { data: this.alignmentNum[index] })
        this.$message.success('保存成功')
        this.tableBtnLoading = false
        this.getList()
        this.$store.dispatch('settings/operateTypeSetting', this.alignmentNum[index].id ? '修改' : '新增')
      } catch (e) {
        this.tableBtnLoading = false
      }
    },
    deleteFun(id) {
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (!id) {
          this.$message('请先点击使用')
          return
        }
        routingSchema('delete', id, { data: { id: id }})
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
}
</style>
