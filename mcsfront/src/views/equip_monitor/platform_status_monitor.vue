<template>
  <div class="platform_status_monitor">
    <!-- 站台状态监控 未使用-->
    <div style="padding:15px;background: rgb(211,216,210);">
      <div
        v-for="(item, index) in itemsVehicle"
        :key="item.label"
        style="display:inline-block;margin-right:10px"
      >
        <el-tag
          size="mini"
          effect="dark"
          :style="{'background':colorVehicle[index],'color':'#FFF','width':'40px','text-align':'center'}"
          @click="clickVehicle(item)"
        >
          {{ state_cnt_dict[item.label]?state_cnt_dict[item.label]:0 }}
        </el-tag>
        <span
          class="pointer"
          :style="{'color':item.textColor?item.textColor:'#000'}"
          @click="clickTask(item.label)"
        >
          {{ item.label }}
        </span>
      </div>
      <span style="margin:0;font-weight: 800;">站台总数:{{ total_cnt }}</span>

    </div>
    <el-row :gutter="5">
      <el-col :span="13"><div class="grid-content bg-purple">
        <el-tabs v-model="activeName" type="card" tab-position="left" style="height:80vh;width: 130px;display: inline-block;float: left;" @tab-click="clickTabs">
          <el-tab-pane v-for="item in process_list" :key="item.id" :label="item.process_name" :name="item.id" />
        </el-tabs>
        <div class="itemClass" style="margin-left: 130px;overflow-y: scroll;max-height:84vh">
          <div v-for="(itemFa,itemFaKey,i) in tableData" :key="i" style="overflow: hidden;">
            <h3 v-if="JSON.stringify(itemFa) !== '{}'">{{ itemFaKey }}</h3>
            <div v-for="(itemVehicle,itemVehicleKey) in itemFa" :key="itemVehicleKey" class="equip-box">
              <div class="equip-box-title">{{ itemVehicleKey }}</div>
              <div
                v-for="(item,indexItem) in itemVehicle"
                :key="item.id"
                :class="[currentIndex===indexItem&&currentFaIndex===itemVehicleKey?'border-style':'','box-style']"
                :style="{'background':itemsVehicle.find(d=>d.label === item.state).color}"
                @click="clickBox(indexItem,itemVehicleKey,item)"
              >{{ item.platform_name }}</div>
            </div>
          </div>
        </div>
      </div></el-col>
      <el-col :span="11"><div class="grid-content bg-purple">
        <el-form :inline="true">
          <el-form-item label="站台号" style="margin-bottom: 10px;padding-right: 40px;">
            {{ rightTableData.platform_code }}
          </el-form-item>
          <el-form-item label="任务号" style="margin-bottom: 10px;padding-right: 40px;">
            {{ rightTableData.task_no }}
          </el-form-item>
          <el-form-item label="AGV" style="margin-bottom: 10px;padding-right: 40px;">
            {{ rightTableData.agv_no }}
          </el-form-item>
        </el-form>
        <el-card v-for="(item,index) in rightTableData.basket_data" :key="index" class="box-card-w" style="margin-bottom:3px !important">
          <div style="padding-right:1%">
            <span v-for="itemFive in 5" :key="itemFive" :class="['five-box',item.current_basket_num+1>itemFive?'five-box-green':'']" />
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">部件号</span>
            <span style="width:30%;display: inline-block;">{{ item.part_code }}</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">手自动状态</span>
            <span style="width:30%;display: inline-block;">{{ item.state }}</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">任务类型</span>
            <span style="width:30%;display: inline-block;">{{ item.task_type }}</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">当前花篮数量</span>
            <span style="width:30%;display: inline-block;">{{ item.current_basket_num }}</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">阈值数量</span>
            <span style="width:30%;display: inline-block;">{{ item.threshold }}</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">自动生产任务剩余花篮数量</span>
            <span style="width:30%;display: inline-block;">o</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">设置延时等待时间</span>
            <span style="width:30%;display: inline-block;">o</span>
          </div>
          <div class="text item">
            <span style="width:70%;display: inline-block;">当前延时等待时间</span>
            <span style="width:30%;display: inline-block;">o</span>
          </div>
          <div v-if="item.task_type==='卸货'" class="arrowRight"><i class="el-icon-right" /></div>
          <div v-else class="arrowRight"><i class="el-icon-back" /></div>
        </el-card>
      </div></el-col>
    </el-row>
  </div>
</template>

<script>
import { productionProcesses, monitorPlatform, monitorPlatformDetail } from '@/api/base_w'
export default {
  name: 'PlatformStatusMonitor',
  data() {
    return {
      colorVehicle: ['#48b596', '#95c454', '#f1b253', '#3d40c3', '#e06377', '#4ea8dc', '#d33e47'],
      itemsVehicle: [
        { type: 2, label: '空闲', color: '#48b596' },
        { type: 3, label: '任务', color: '#95c454' },
        { type: 4, label: '异常', color: '#f1b253' },
        { type: 5, label: '开启对接站台', color: '#3d40c3' }
      ],
      getParams: {},
      total_cnt: 0,
      state_cnt_dict: {},
      loading: false,
      activeName: '0',
      currentIndex: null,
      obj: null,
      currentFaIndex: '',
      process_list: [],
      tableData: [],
      rightTableData: [],
      statisticalQuantity: []
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/platform-status-monitor') {
          this.getOtherList()
          this._setInterval = setInterval(d => {
            if (this.currentIndex !== null) {
              this.clickBox(this.currentIndex, this.currentFaIndex, this.item)
            }
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
    // this.getOtherList()
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  methods: {
    clickTask(val) {
      this.getParams.filter_state = val
      this.itemsVehicle.forEach(d => {
        if (d.label === val) {
          if (d.textColor) {
            delete d.textColor
            delete this.getParams.filter_state
          } else {
            d.textColor = '#5A9CF8'
          }
        } else {
          delete d.textColor
        }
      })
      this.currentIndex = null
      this.currentFaIndex = null
      this.rightTableData = []
      this.getList()
    },
    async getOtherList() {
      try {
        const a = await Promise.all([
          productionProcesses('get', null, { params: { all: 1, is_used: true }})
        ])
        this.process_list = a[0] || []
        this.process_list.forEach(d => {
          d.id = (d.id).toString()
        })
        this.process_list.unshift({ process_name: '全部', id: '0' })
        this.getList()
      } catch (e) {
        //
      }
    },
    async getList() {
      try {
        // this.currentIndex = null
        // this.currentFaIndex = null
        // this.rightTableData = []
        this.loading = true
        this.getParams.process_id = this.activeName === '0' ? '' : this.activeName
        const data = await monitorPlatform('get', null, { params: this.getParams })
        this.tableData = data.data || []
        this.state_cnt_dict = data.state_cnt_dict
        this.total_cnt = data.total_cnt
        this.loading = false

        const arr = [0, 0, 0, 0]
        for (const key in this.tableData) {
          if (Object.hasOwnProperty.call(this.tableData, key)) {
            const element = this.tableData[key]
            for (const key1 in element) {
              if (Object.hasOwnProperty.call(element, key1)) {
                const element1 = element[key1]
                element1.forEach(dd => {
                  if (dd.state === '空闲') {
                    arr[0] += 1
                  }
                  if (dd.state === '任务') {
                    arr[1] += 1
                  }
                  if (dd.state === '异常') {
                    arr[2] += 1
                  }
                  if (dd.state === '开启对接站台') {
                    arr[3] += 1
                  }
                })
              }
            }
          }
        }
        this.statisticalQuantity = arr
      } catch (e) {
        this.loading = false
      }
    },
    async clickBox(index, faIndex, item) {
      this.currentIndex = index
      this.currentFaIndex = faIndex
      this.obj = item
      try {
        const data = await monitorPlatformDetail('get', null, { params: { platform_id: item.id }})
        this.rightTableData = data || []
      } catch (e) {
        //
      }
    },
    clickTabs() {
      this.currentIndex = null
      this.currentFaIndex = null
      this.rightTableData = []
      this.getList()
    }
  }
}
</script>

  <style lang="scss">
  .platform_status_monitor{
    // .el-tabs__nav-scroll{
      // position: fixed;
    // }
    .itemClass{
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
    .pointer{
        cursor: pointer;
    }
    .equip-box{
        background: rgb(136, 135, 135);
        // margin-left: 150px;
        width: 49%;
        padding-left:8px;
        padding-bottom:8px;
        margin-right: 1%;
        margin-bottom: 15px;
        color: #fff;
        display: inline-block;
    }
    .equip-box-title{
        padding:8px 0;
        border-bottom: 1px solid #fff;
        font-size: 16px;
    }
    .border-style{
        border:3px dashed #000;
        line-height: 33px !important;
    }
    .box-style{
        width: 95%;
        height: 40px;
        display: inline-block;
        margin:8px 2px 0 3px;
        line-height: 40px;
        padding-left:5px;
        color: #fff;
        font-size: 16px;
        overflow: hidden;
    }
    .box-card-w{
    position: relative;
    width: 50%;
    display: inline-block;
  }
  .arrowRight{
    position:absolute;
    top:50px;
    left:45%;
    font-size: 40px;
    color: rgb(225, 118, 118);
  }
  .five-box{
    display: inline-block;
    margin-left: 1%;
    margin-top: 10px;
    width:19%;
    height: 50px;
    background: #eee;
  }
  .five-box-green{
    background: forestgreen;
  }
  .text{
    margin-bottom: 8px;
    margin-top: 8px;
  }
}
  </style>
