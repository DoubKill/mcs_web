<template>
  <div>
    <!-- AGV状态监控 -->
    <!-- <el-tabs
      v-model="cycle_location_name"
      class="w-tabs-style"
      @tab-click="handleClick"
    >
      <el-tab-pane
        label="全部"
        name="all"
      />
      <el-tab-pane
        v-for="(item, index) in tabHearder"
        :key="index"
        :label="item.global_name"
        :name="item.global_name"
      />
    </el-tabs> -->

    <el-row :gutter="10" style="margin-top:10px">
      <el-col :span="12" style="min-height:90vh">
        <div class="w-tabs-style grid-content bg-purple">
          <div class="top-search-box" style="padding:3px 10px;background: #DCD7D1;">
            <el-form :inline="true">
              <el-form-item>
                <h5 style="margin:0">小车总数：{{ total_cnt }}</h5>
              </el-form-item>
            </el-form>
            <div v-for="(item, index) in itemsVehicle" :key="item.label" style="display:inline-block;margin-right:10px">
              <el-tag size="mini" effect="dark" :style="{'background':colorVehicle[index],'color':'#FFF','width':'40px','text-align':'center'}">
                {{ state_cnt_dict[item.type]?state_cnt_dict[item.type]:0 }}
              </el-tag>
              <span class="pointer" :style="{'color':item.color?item.color:'#000'}" @click="clickTask(item.type)">
                {{ item.label }}</span>
            </div>
          </div>
          <div style="max-height: 75vh;overflow-y:auto">
            <div v-for="(item,index) in leftData" :key="item.id" :style="{'background':colorVehicle[itemsVehicle.find(d=>d.type===item.state).type-1]}" :class="[currentIndex===index?'border-style':'','box-style']" class="vehicleCodeStyle" @click="clickBox(index,item.vehicle_id)">
              <!-- {{ item.vehicle_code }}
              <div class="electricityStyle" :style="{'background-position':`0px ${item.battery_percent<=20?'1px':item.battery_percent<=40?'-16px':item.battery_percent<=60?'-34px':item.battery_percent<=80?'-52px':'-70px'}`}"> {{ item.battery_percent }}</div> -->

              <div style="width:60%;border-right: 1px solid #DCD7D1;text-align: center;box-sizing: border-box;line-height: auto;">
                {{ item.vehicle_code }}
                <div class="electricityStyle" :style="{'background-position':`0px ${item.battery_percent<=20?'1px':item.battery_percent<=40?'-16px':item.battery_percent<=60?'-34px':item.battery_percent<=80?'-52px':'-70px'}`}">{{item.battery_percent}}</div>
              </div>
              <div style="width:40%;font-size:12px;text-align: center;">
                <div style="height:30px;padding-top: 5px;line-height: 2;">
                  {{ item.upper_full?'满':'空' }}
                </div>
                <div style="border-top: 1px solid #DCD7D1;height:30px;line-height: 30px;">
                  {{ item.lower_full?'满':'空' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card" style="width:95%">
          <div slot="header" class="clearfix">
            <span>AGV信息</span>
          </div>
          <div style="display:flex">
            <el-col :span="12">
              <div class="text item">
                <span style="width:50%;display: inline-block;">小车号</span>
                <span style="width:50%;display: inline-block;">{{ agvData.agv_no }}</span>
              </div>
              <div class="text item">
                <span style="width:50%;display: inline-block;">小车状态</span>
                <span style="width:50%;display: inline-block;">{{ itemsVehicle.find(d=>d.type === agvData.state)?itemsVehicle.find(d=>d.type === agvData.state).label:'' }}</span>
              </div>
              <div class="text item">
                <span style="width:50%;display: inline-block;">电量</span>
                <span style="width:50%;display: inline-block;">{{ agvData.battery_percent }}</span>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="text item">
                <span style="width:50%;display: inline-block;">任务号</span>
                <span style="width:50%;display: inline-block;">{{ agvData.task_no }}</span>
              </div>
              <div class="text item">
                <span style="width:50%;display: inline-block;">当前位置</span>
                <span style="width:50%;display: inline-block;">{{ agvData.location_code }}</span>
              </div>
            </el-col>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12" style="padding-left:0">
        <div class="grid-content bg-purple">
          <el-card v-for="(item,index) in agvData.basket_data" :key="index" class="box-card" style="margin-bottom:3px !important">
            <div slot="header" class="clearfix">
              <span>{{ '轴'+ (index + 1) }}</span>
            </div>
            <div v-for="(itemBox,index1) in agvData.basket_nums" :key="itemBox" :class="['five-box',index1<item.num?'five-box-green':'']" :style="{'width':(100-agvData.basket_nums)/agvData.basket_nums+'%'}" />
            <div class="text item">
              <span style="width:40%;display: inline-block;">工艺段</span>
              <span style="width:60%;display: inline-block;">{{ item.process }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">来源站台</span>
              <span style="width:60%;display: inline-block;">{{ item.machine_no }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">包号</span>
              <span style="width:60%;display: inline-block;">{{ item.material_type }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">下料时间</span>
              <span style="width:60%;display: inline-block;">{{ item.out_time }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">Qtime(s)</span>
              <span style="width:60%;display: inline-block;">{{ item.qtime }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">库存花篮数量</span>
              <span style="width:60%;display: inline-block;">{{ agvData.basket_nums }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">实际花篮数量</span>
              <span style="width:60%;display: inline-block;">{{ agvData.basket_data.find(d=> { return d.axis===index+1 }).num }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">是否超期</span>
              <span style="width:60%;display: inline-block;">
                <el-tag size="mini" v-if="item.out_time&&item.qtime" style="border-radius: 20px" effect="dark" :type="setOverdue(item.out_time,item.qtime)?'danger':'info'">{{ setOverdue(item.out_time,item.qtime)?'是':'否' }}</el-tag>
              </span>
            </div>
            <!-- <div
            v-if="agvData.basket_nums>0"
            class="taskTips"
          >
            任务号<br>
            {{ item.task_no }}
          </div> -->
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getGlobalCodes } from '@/api/basics'
import { agvMonitor, agvDetailMonitor } from '@/api/jqy'
export default {
  name: 'AgvMonitor',
  data() {
    return {
      agvData: { basket_data: [] },
      cycle_location_name: 'all',
      activeName: 'first',
      total_cnt: 0,
      state_cnt_dict: {},
      leftData: [],
      colorVehicle: ['#656f71', '#48b596', '#95c454', '#4ea8dc', '#d33e47'],
      getParams: {},
      vehicle_id: null,
      tabHearder: [],
      itemsVehicle: [
        { type: 1, label: '离线' },
        { type: 2, label: '空闲' },
        { type: 3, label: '任务' },
        { type: 4, label: '充电' },
        { type: 5, label: '故障' }
      ],
      currentIndex: null
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/agv-monitor') {
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
            if (this.currentIndex !== null) {
              this.clickBox(this.currentIndex, this.vehicle_id)
            }
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
    // this.getList()
    this.getHeaderList()
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await agvMonitor('get', null, { params: this.getParams })
        this.leftData = data.data || []
        this.state_cnt_dict = data.state_cnt_dict
        this.total_cnt = data.total_cnt
        // this.agvData = []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async getHeaderList() {
      try {
        const data = await getGlobalCodes({ all: 1, type_name: '工艺循环' })
        this.tabHearder = data || []
      } catch (e) {
        //
      }
    },
    clickTask(val) {
      this.getParams.filter_state = val
      this.itemsVehicle.forEach(d => {
        if (d.type === val) {
          if (d.color) {
            delete d.color
            delete this.getParams.filter_state
          } else {
            d.color = '#5A9CF8'
          }
        } else {
          delete d.color
        }
      })
      this.currentIndex = null
      this.agvData = []
      this.getParams.vehicle_id = val.vehicle_id
      this.getList()
    },
    handleClick() {
      this.getParams.cycle_location_name = this.cycle_location_name
      if (this.getParams.cycle_location_name === 'all') {
        delete this.getParams.cycle_location_name
      }
      this.currentIndex = null
      this.agvData = []
      this.getList()
    },
    async clickBox(index, vehicle_id) {
      try {
        this.currentIndex = index
        this.vehicle_id = vehicle_id
        const data = await agvDetailMonitor('get', null, { params: { vehicle_id: vehicle_id } })
        this.agvData = data || []
      } catch (e) {
        //
      }
    },
    setOverdue(out_time, qtime) {
      var date = Date.parse(new Date(out_time));
      let dateC = Date.parse(new Date());
      let dateQ = date + qtime * 1000
      if (dateQ < dateC) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
    .w-tabs-style{
        margin-left:15px;
    }
    // .el-tag--dark{
    //     cursor: pointer;
    // }
    .pointer{
        cursor: pointer;
    }
    .box-style{
        width: 19%;
        height: 60px;
        display: inline-block;
        margin:6px 0.5% 0 0.5%;
        // line-height: 40px;
        padding-left:5px;
        color: #fff;
        font-size: 18px;
        overflow: hidden;
    }
    .border-style{
        border:3px dashed #000;
        // line-height: 32px;
    }
    .item {
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 10px;
  }
  .box-card{
    position: relative;
    width: 46%;
    display: inline-block;
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
    background: #9CCB5C;
  }
  .taskTips{
    position: absolute;
    top:120px;
    right:10px;
    padding:5px 10px;
    height: 50px;
    line-height:20px;
    box-shadow: 0 4px 6px rgb(0, 0, 0);
  }
  .electricityStyle{
    background:url('../../assets/battery.png')  0 1px no-repeat;
    width: 60px;
    height: 20px;
    display: inline-block;
    text-align: right;
    line-height: 20px;
    margin-right: 12px;
    margin-left: 5px;
    color: #000;
    font-size: 15px;
  }
  .vehicleCodeStyle{
    display:  inline-flex;
    justify-content: space-between;
    align-items: center;
    overflow: hidden;
  }
</style>
