<template>
  <div class="platform_status">
    <!-- 站台状态监控 -->
    <div style="padding:15px;">
      站台状态：
      <div v-for="(item) in itemsVehicle" :key="item.label" style="display:inline-block;margin-right:20px">
        <el-button v-if="item.type" size="medium" :style="{'background':item.color,'color':'#FFF','text-align':'center','vertical-align': 'middle'}" circle />
        <svg-icon v-else icon-class="network_unl" class="networkStyle" />
        <span class="pointer" :style="{'color':item.textColor?item.textColor:'#000'}">
          {{ item.label }}
        </span>
      </div>
      任务状态：
      <div v-for="(item) in agvColor" :key="item.label" style="display:inline-block;margin-right:20px">
        <el-button size="medium" :style="{'background':item.color,'color':'#FFF','text-align':'center','vertical-align': 'middle','border-radius': '0'}" circle />
        <span class="pointer" :style="{'color':item.textColor?item.textColor:'#000'}">
          {{ item.label }}
        </span>
      </div>
      <el-checkbox-group v-model="checkList" style="display:inline-block" @change="changeChecked">
        <el-checkbox label="1">隐藏站台</el-checkbox>
        <el-checkbox label="2">隐藏堆栈</el-checkbox>
        <!-- <el-checkbox label="3">隐藏休息位</el-checkbox> -->
      </el-checkbox-group>
      <el-form :inline="true">
        <el-form-item label="工作区" style="margin-bottom:0">
          <el-select v-model="workspace_search" clearable size="small" placeholder="请选择" @visible-change="getOtherList" @change="changeFun">
            <el-option v-for="item in workspaceList" :key="item.id" :label="item.area_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="工序段" style="margin-bottom:0">
          <el-select multiple v-model="process_search" clearable size="small" placeholder="请选择" style="width:400px" @change="changeFun">
            <el-option v-for="item in headListCopy" :key="item.process_name" :label="item.process_name" :value="item.process_name" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    <div class="platformStatusContent">
      <div v-for="(val,key) in headList" :key="key" class="topCard">
        <div class="topOne">{{ val.process_name }}</div>
        <div style="display:flex;justify-content:space-between">
          <div class="topTwo topTwoAgv">AGV</div>
          <div class="topTwo">上层
            <i :class="val.upper_rail_type===1?'el-icon-top':val.upper_rail_type===2?'el-icon-bottom':''" />
          </div>
          <div class="topTwo">下层
            <i :class="val.lower_rail_type===1?'el-icon-top':val.lower_rail_type===2?'el-icon-bottom':''" />
          </div>
        </div>
        <div v-for="(item,_key) in tableData[val.process_name]" :key="_key">
          <!-- <div v-for="(itemFa,keyFa) in tableData" :key="keyFa" :style="{'min-height':(maxHeight[keyFa]*61 + 16)+'px'}"> -->
          <!-- 61 -->
          <!-- <span v-if="key===0" class="goldenLineStyle">
            <span class="goldenLineStyle0">{{ keyFa }}</span>
            <span class="borderGoldenLineStyle borderGoldenLineStyle0" />
          </span>
          <span v-else class="goldenLineStyle borderGoldenLineStyle">{{ '' }}</span> -->
          <!-- <div v-if="itemFa[val.process_name]&&itemFa[val.process_name].length===0" style="" /> -->
          <!-- <div v-for="(item,_key) in itemFa[val.process_name]" :key="_key" style="padding-top: 5px;"> -->

          <div class="topTwo carBox" :style="{'background':item.dp_type===1?'#f8d4e6':item.dp_type===2?'#bed5e9':'#bcffa5'}">
            <el-popconfirm title="改变设备屏蔽状态" icon="el-icon-info" confirm-button-text="屏蔽" cancel-button-text="不屏蔽" @onConfirm="confirmFun(item)" @onCancel="cancelFun(item)">
              <svg-icon :slot="'reference'" v-if="item.dp_type===2&&!item.is_connected" icon-class="network_unl" class="networkStyle referenceNetworkStyle" />

              <el-button v-else-if="item.dp_type===1&&item.plt_state!==0" :slot="'reference'" :style="{'background':itemsVehicle.find(d=>d.type===item.plt_state)?itemsVehicle.find(d=>d.type===item.plt_state).color:'transparent','float': 'left','padding': '9px', 'margin-top': '-1px','border':'none'}" circle />
              <svg-icon :slot="'reference'" v-else-if="item.dp_type===1&&item.plt_state===0" icon-class="network_unl" class="networkStyle referenceNetworkStyle" />
              <el-button v-else-if="item.dp_type!==1&&item.in_plt_state!==0" :slot="'reference'" :style="{'background':itemsVehicle.find(d=>d.type===item.in_plt_state)?itemsVehicle.find(d=>d.type===item.in_plt_state).color:'transparent','float': 'left','padding': '9px', 'margin-top': '-1px','border':'none'}" circle />
              <svg-icon :slot="'reference'" v-else-if="item.dp_type!==1&&item.in_plt_state===0" icon-class="network_unl" class="networkStyle referenceNetworkStyle" />
            </el-popconfirm>
            <el-popconfirm v-if="item.dp_type===2&&item.is_connected" title="改变设备屏蔽状态" icon="el-icon-info" confirm-button-text="屏蔽" cancel-button-text="不屏蔽" @onConfirm="confirmFun1(item,1)" @onCancel="confirmFun1(item,2)">
              <el-button v-if="item.out_plt_state" :slot="'reference'" :style="{'background':itemsVehicle.find(d=>d.type===item.out_plt_state)?itemsVehicle.find(d=>d.type===item.out_plt_state).color:'transparent','float': 'left','padding': '9px','margin-left': '5px', 'margin-top': '-1px','border':'none'}" circle />
              <svg-icon :slot="'reference'" v-else icon-class="network_unl" class="networkStyle referenceNetworkStyle" />
            </el-popconfirm>
            <span class="spanTitle" :title="item.instance_name" style="cursor: default;">{{ item.instance_name }}</span>
            <span v-if="item.dp_type===2" style="margin-left:5px">{{ item.used_locations }}/{{ item.total_locations }}</span>
            <svg-icon :style="{'color':item.alarm_flag===1?'#f3a647':item.alarm_flag===2?'red':'transparent'}" icon-class="warnSVG" class="warningStyle" />
          </div>
          <div style="height:30px;display:flex;justify-content:space-between">
            <!-- 第一个方块 里面2个小方块-->
            <div class="topTwo agvBoxFa topTwoAgv">
              <span v-if="item.dp_type===1" :style="{'background':agvColor.find(d=>d.type===item.task_state)?agvColor.find(d=>d.type===item.task_state).color:'#fff'}" class="agvBox">{{ item.agv_no }}</span>
              <span v-else-if="item.dp_type===2" :style="{'background':agvColor.find(d=>d.type===item.up_task_state)?agvColor.find(d=>d.type===item.up_task_state).color:'#fff'}" class="agvBox">{{ item.up_agv_no }}</span>
              <span v-else>{{ item.agv_no }}</span>

              <span v-if="item.dp_type===1" style="display:none" class="agvBox agvBoxRight">{{ }}</span>
              <span v-else-if="item.dp_type===2" :style="{'background':agvColor.find(d=>d.type===item.down_task_state)?agvColor.find(d=>d.type===item.down_task_state).color:'#fff'}" class="agvBox agvBoxRight">{{ item.down_agv_no }}</span>
              <span v-else>{{ }}</span>
            </div>
            <!-- 第二个方块 类型1使用 里面2个方块-->
            <div v-if="item.dp_type===1" class="basketNumTow">
              <div class="basketNum" :style="{'border-color':(item.upper_rail_num||item.upper_rail_num||item.upper_trigger_threshold)?'#eee':'#fff'}">
                <span class="dottedLine" :style="{'left':!item.upper_trigger_threshold&&item.upper_trigger_threshold!==0?'-30000px':item.upper_trigger_threshold*10+'%'}" />
                <span class="progressStyle" :style="{'background':item.lower_rail_state?'#b6b2b2':'','width':item.lower_rail_state?'100%':item.upper_rail_num*10+'%'}" />
                <span :style="{'z-index':'1','position': 'inherit','background':item.lower_rail_state?'#b6b2b2':''}">{{ item.upper_rail_num }}</span>
              </div>
              <div class="basketNum" :style="{'border-color':(item.lower_rail_num||item.lower_rail_num||item.lower_trigger_threshold)?'#eee':'#fff'}">
                <span class="dottedLine" :style="{'left':!item.lower_trigger_threshold?'-30000px':item.lower_trigger_threshold*10+'%'}" />
                <span class="progressStyle" :style="{'background':item.upper_rail_state?'#b6b2b2':'','width':item.upper_rail_state?'100%':item.lower_rail_num*10+'%'}" />
                <span :style="{'z-index':'1','position': 'inherit','background':item.lower_rail_state?'#b6b2b2':''}">{{ item.lower_rail_num }}</span>
              </div>
            </div>
            <!-- 第二个方块 只在休息位使用 里面1个大方块-->
            <div v-else-if="item.dp_type===2&&item.process_used_locations" class="basketNumOwn">{{ item.process_used_locations }}</div>
          </div>
        </div>
        <!-- </div> -->
      </div>
    </div>

    <el-dialog title="列表" :visible.sync="dialogVisible" width="500px" :before-close="handleClose">
      <el-table v-loading="dialogLoading" :data="tableData1" border style="width: 100%">
        <el-table-column prop="date" label="日期" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { equipStatus, workAreas } from '@/api/base_w'
import { platformInfoNewUpdate, cacheDeviceInfo } from '@/api/jqy'
export default {
  name: 'PlatformStatus',
  data() {
    return {
      itemsVehicle: [
        { type: 4, label: '已屏蔽', color: '#B1B3B4' },
        { type: 1, label: '正常生产', color: '#95c454' },
        { type: 2, label: '缺料', color: '#f1b253' },
        { type: 3, label: '故障', color: 'red' },
        { type: 5, label: '其他', color: '#3d40c3' },
        { type: 0, label: '断连', color: '#409eff' }
      ],
      agvColor: [
        { type: 1, label: '已创建', color: 'rgb(188 126 227)' },
        { type: 2, label: '已下发', color: '#b78992' },
        { type: 3, label: '已指派AGV', color: '#43a4a3' },
        { type: 4, label: 'AGV已到达', color: '#ea73aa' }
      ],
      bottomCardData: [],
      tableData: null,
      dialogVisible: false,
      tableData1: [],
      dialogLoading: false,
      headList: [],
      maxHeight: {},
      checkList: [],
      process_search: [],
      headListCopy: [],
      workspaceList: [],
      workspace_search: null
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/platform-status') {
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
          }, 5000)
        } else {
          window.clearInterval(this._setInterval)
        }
      },
      deep: true, // 深度监听
      immediate: true // 第一次初始化渲染就可以监听到
    }
  },
  created() {
  },
  methods: {
    async getList() {
      try {
        let _str = ''
        if (this.checkList && this.checkList.length > 0) {
          _str = this.checkList.join(',')
        }
        this.loading = true
        const data = await equipStatus('get', null, { params: { dp_type: _str, working_area_id: this.workspace_search } })
        this.headListCopy = data.table_head
        this.tableData = data.table_data

        // 计算一条线最高数量
        this.maxHeight = {}
        for (const key in data.table_data) {
          if (Object.hasOwnProperty.call(data.table_data, key)) {
            const element = data.table_data[key]
            let maxNum = 0
            for (const key1 in element) {
              if (Object.hasOwnProperty.call(element, key1)) {
                const element1 = element[key1]
                if (element1.length > maxNum) {
                  maxNum = element1.length
                }
              }
            }
            this.maxHeight[key] = maxNum
          }
        }

        // 工序过滤
        if (this.process_search.length > 0) {
          let arr = this.headListCopy.filter(d => {
            return this.process_search.findIndex(D => D === d.process_name) > -1
          })
          this.headList = arr
        } else {
          this.headList = this.headListCopy
        }
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    changeChecked() {
      this.getList()
    },
    changeFun() {
      this.getList()
    },
    confirmFun(item) {
      // 屏蔽
      let _val = '禁用屏蔽'
      let arr = item.plt_state !== 4 ? [item.instance_id] : ''
      if (arr.length === 0) {
        this.$message('已屏蔽')
        return
      }
      if (item.dp_type === 3) {
        this.$message('无此屏蔽功能')
      } else if (item.dp_type === 1) {
        platformInfoNewUpdate('post', null, { data: { 'obj_ids': arr } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', _val)
            this.getList()
          }).catch(() => {
          })
      } else {
        // 堆栈屏蔽
        cacheDeviceInfo('patch', item.instance_id, { data: { 'in_is_used': false } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', _val)
            this.getList()
          }).catch(() => {
          })
      }
    },
    cancelFun(item) {
      let _val = '启用'
      let arr = item.plt_state === 4 ? [item.instance_id] : ''
      if (item.dp_type === 3) {
        this.$message('无此屏蔽功能')
      } else if (item.dp_type === 1) {
        if (arr.length === 0) {
          this.$message('已启用')
          return
        }
        platformInfoNewUpdate('post', null, { data: { 'obj_ids': arr } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', _val)
            this.getList()
          }).catch(() => {
          })
      } else {
        // 堆栈屏蔽
        cacheDeviceInfo('patch', item.instance_id, { data: { 'in_is_used': true } })
          .then((response) => {
            this.$message({
              type: 'success',
              message: '操作成功!'
            })
            this.$store.dispatch('settings/operateTypeSetting', _val)
            this.getList()
          }).catch(() => {
          })
      }
    },
    confirmFun1(item, type) {
      // 堆栈屏蔽
      let _val = type === 1 ? '禁用屏蔽' : '启用'
      cacheDeviceInfo('patch', item.instance_id, { data: { 'out_is_used': type === 1 ? false : true } })
        .then((response) => {
          this.$message({
            type: 'success',
            message: '操作成功!'
          })
          this.$store.dispatch('settings/operateTypeSetting', _val)
          this.getList()
        }).catch(() => {
        })
    },
    showListFun() {
      this.dialogVisible = true
      this.getDialogList()
    },
    getDialogList() {

    },
    handleClose(done) {
      this.dialogVisible = false
      if (done) {
        done()
      }
    },
    async getOtherList(val) {
      if (val) {
        try {
          const a = await workAreas('get', null, { params: { all: 1 } })
          this.workspaceList = a || []
        } catch (e) {
          //
        }
      }
    },
  }
}
</script>

<style lang="scss" scoped>
.platformStatusContent{
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    height: 79vh;
    // padding-left: 100px;

    .topCard{
    color: #000;
    display:inline-block;
    margin-left: 3px;
      margin-right: 3px;
    .topOne{
        padding:0 5px;
      text-align: center;
      color:#fff;
      background: rgb(86,80,119);
      line-height: 30px;
      width: 180px;
      height: 30px;
      text-overflow:ellipsis;
      white-space: nowrap;
    overflow: hidden;
    }
    .bottomOne{
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
      width: 85px;
      height: 40px;
    }
  }
    .bottomCard{
      margin-left: 10px;
      margin-right: 20px;
      margin-top: 10px;
      float: left;
      .leftOne{
        width: 85px;
        min-height: 40px;
        float: left;
      }
      .rightOne{
        margin-left: 10px;
        min-height: 40px;
        width: 85px;
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
        width: 85px;
        padding: 7px;
        white-space: pre-wrap;
        font-size: 13px;
      }
    }
    .topTwo{
        width:34%;
        background: rgb(188, 184, 184);
        text-align: center;
        padding: 5px;
        color: #fff;
    }
    .topTwoAgv{
      width:30%;
    }
    .agvBoxFa{
      padding: 0px;
      display: flex;
      background: #fff;
    }
    .agvBox{
      color:#000;
      // border: 1px solid #eee;
      width:50%;
      height: 100%;
      text-align: center;
      line-height: 30px;
      display: inline-block;
      // background: #fff;
    }
    .agvBoxRight{
      margin-left:1px;
    }
    .carBox{
        width: 130px;
        white-space: nowrap;
        width:100%;
        // margin-top:5px;
        color: #000;
      cursor: pointer;
    }
    .el-icon-top , .el-icon-bottom{
      color: #000;
      font-weight: 700;
    }
    .warningStyle{
      float: right;
      font-size: 18px;
      margin-top: -1px;
    }
    .basketNumOwn{
      display: inline-block;
      width:70%;
      border: 1px solid #eee;
      height: 100%;
      text-align: center;
      line-height: 30px;
      cursor: pointer;
    }
    .basketNum{
      display: inline-block;
      width:49%;
      border: 1px solid #fff;
      height: 100%;
      text-align: center;
      line-height: 30px;
      position: relative;
    }
    .dottedLine{
      display: inline-block;
      height: 100%;
      position:absolute;
      left:-30000px;
      border: 0.5px dashed #000;
      z-index:1;
    }
    .progressStyle{
      display: inline-block;
      position:absolute;
      left:0;
      height: 100%;
      background: #c4f1c8;
    }
    .basketNumTow{
      width:69%;
      display:flex;
      justify-content:space-between;
    }
    .goldenLineStyle{
      width: 90px;
      max-height: 16px;
      // float: left;
      margin-left: -95px;
      display: inline-block;
      white-space: normal;
      position: relative;
    }
    .borderGoldenLineStyle{
      width: 200%;
      border:0.5px solid #eee;
      margin-left:-185px;
      display: inline-block;
    }
    .goldenLineStyle0{
      position: absolute;
      top: 15px;
    }
    .borderGoldenLineStyle0{
      border:0.5px solid #eee;
      margin-left:0;
    }
    .spanTitle{
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      display: inline-block;
      width: 60px;
    }
}
    .networkStyle{
      font-size: 25px;vertical-align: middle;
    }
    .referenceNetworkStyle{
      margin-top: -3px;
      margin-left: -4px;
      float: left;
    }
</style>
