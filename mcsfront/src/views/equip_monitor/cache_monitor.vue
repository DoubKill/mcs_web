<template>
  <div>
    <!-- 缓存位监控 -->
    <el-tabs
      v-model="district"
      class="w-tabs-style"
      @tab-click="handleClick"
    >
      <el-tab-pane
        label="全部"
        name="all"
      />
      <!-- <el-tab-pane
        v-for="(item, index) in tabHearder"
        :key="index"
        :label="item.district_name"
        :name="item.id.toString()"
      /> -->
    </el-tabs>

    <el-row :gutter="10">
      <el-col :span="12">
        <div class="w-tabs-style grid-content bg-purple">
          <div
            class="top-search-box"
            style="padding:3px 10px;background: #DCD7D1;"
          >
            <el-form :inline="true">
              <el-form-item label="缓存位号">
                <el-input
                  v-model="getParams.location_code"
                  size="small"
                  clearable
                  placeholder="缓存位号"
                  @input="changeDebounce"
                />
              </el-form-item>
              <el-form-item label="AGV编号">
                <el-select
                  v-model="getParams.agv_id"
                  clearable
                  filterable
                  size="small"
                  placeholder="请选择AGV编号"
                  @change="getList"
                  @visible-change="getRack"
                >
                  <el-option
                    v-for="item in rack_list"
                    :key="item.rack_name"
                    :label="item.rack_name"
                    :value="item.id"
                  />
                </el-select>
                <!-- <el-input
                  v-model="getParams.agv_id"
                  size="small"
                  clearable
                  placeholder="AGV编号"
                  @input="changeDebounce"
                /> -->
              </el-form-item>
              <el-form-item>
                <h5 style="margin:0">缓存位数量：{{ total_cnt }}</h5>
              </el-form-item>
            </el-form>
            <div
              v-for="(item, index) in itemsVehicle"
              :key="item.label"
              style="display:inline-block;margin-right:10px"
            >
              <el-tag
                size="mini"
                effect="dark"
                :style="{'background':colorVehicle[index],'color':'#FFF','width':'40px','text-align':'center'}"
              >
                {{ state_cnt_dict[item.label]?state_cnt_dict[item.label]:0 }}
              </el-tag>
              <span
                class="pointer"
                :style="{'color':item.color?item.color:'#000'}"
                @click="clickTask(item.label)"
              >
                {{ item.label }}
              </span>
            </div>
          </div>
          <div
            class="scorll"
            style="max-height: 75vh;overflow-y:auto"
          >
            <div
              v-for="(item,index) in cacheData"
              :key="item.id"
              :class="[currentIndex===index?'border-style':'','box-style']"
              :style="{'background':colorVehicle[itemsVehicle.find(d=>d.label===item.state).type],'white-space': 'pre-wrap'}"
              @click="clickBox(index,item.id)"
            >{{ item.location_code+`\n` }}{{ (item.rack_name?item.rack_name:item.locked_rack_name)+((item.rack_name?item.rack_name:item.locked_rack_name)?'#AGV':'')+`\n` }}{{ item.left_time+(item.left_time?'s':'')+`\n` }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="grid-content bg-purple">
          <el-card class="box-card">
            <div
              slot="header"
              class="clearfix"
            >
              <span>AGV信息</span>
            </div>
            <div class="text item">
              <span style="width:50%;display: inline-block;">小车号</span>
              <span style="width:50%;display: inline-block;">{{ agvData.agv_no }}</span>
            </div>
            <div class="text item">
              <span style="width:50%;display: inline-block;">小车状态</span>
              <span style="width:50%;display: inline-block;">{{ agvData.state }}</span>
            </div>
            <div class="text item">
              <span style="width:50%;display: inline-block;">任务号</span>
              <span style="width:50%;display: inline-block;">{{ agvData.task_no }}</span>
            </div>
          </el-card><br>
          <el-card
            v-for="(item,index) in agvData.basket_data"
            :key="index"
            class="box-card"
            style="margin-bottom:3px !important"
          >
            <div
              slot="header"
              class="clearfix"
            >
              <span>{{ '轴'+ (index + 1) }}</span>
            </div>
            <div
              v-for="(itemBox,index1) in agvData.basket_nums"
              :key="itemBox"
              :class="['five-box',index1<item.num?'five-box-green':'']"
              :style="{'width':(100-agvData.basket_nums)/agvData.basket_nums+'%'}"
            />
            <div class="text item">
              <span style="width:40%;display: inline-block;">当前工序</span>
              <span style="width:60%;display: inline-block;">{{ item.process }}</span>
            </div>
            <div class="text item">
              <span style="width:40%;display: inline-block;">动作类型</span>
              <span style="width:60%;display: inline-block;">{{ item.action }}</span>
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
              <span style="width:40%;display: inline-block;">物料类型</span>
              <span style="width:60%;display: inline-block;">{{ item.material_type }}</span>
            </div>
            <div
              v-if="agvData.basket_nums>0"
              class="taskTips"
            >
              任务号<br>
              {{ item.task_no }}
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { debounce } from '@/utils'
import { rackInfo } from '@/api/base_w'
import { cacheLocation, cacheLocationDetail } from '@/api/jqy'
export default {
  name: 'CacheMonitor',
  data() {
    return {
      district: 'all',
      agvData: { basket_data: [] },
      activeName: 'first',
      location_id: null,
      total_cnt: 0,
      state_cnt_dict: {},
      colorVehicle: ['#48b596', '#95c454', '#3d40c3', '#d33e47'],
      getParams: {},
      cacheData: [],
      tabHearder: [],
      rack_list: [],
      itemsVehicle: [
        { type: 0, label: '空闲' },
        { type: 1, label: '已占用' },
        { type: 2, label: '锁定' },
        { type: 3, label: '锁定超时' }
      ],
      currentIndex: null
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/cache-monitor') {
          this.getList()
          this._setInterval = setInterval(d => {
            if (this.currentIndex !== null) {
              this.clickBox(this.currentIndex, this.location_id)
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
    // this.getDistrictList()
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  methods: {
    async getRack(val) {
      if (val) {
        try {
          const data = await rackInfo('get', null, { params: { all: 1 }})
          this.rack_list = data || []
        } catch (e) {
        //
        }
      }
    },
    changeDebounce() {
      debounce(this, 'getList')
    },
    async getList() {
      try {
        this.loading = true
        const data = await cacheLocation('get', null, { params: this.getParams })
        this.cacheData = data.data || []
        this.state_cnt_dict = data.state_cnt_dict
        this.total_cnt = data.total_cnt
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    clickTask(val) {
      this.getParams.filter_state = val
      this.itemsVehicle.forEach(d => {
        if (d.label === val) {
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
      this.getList()
    },
    // async getDistrictList() {
    //   try {
    //     const data = await districtInfos('get', null, { params: { all: 1 }})
    //     this.tabHearder = data || []
    //   } catch (e) {
    //     //
    //   }
    // },
    handleClick() {
      this.getParams.district = this.district
      if (this.getParams.district === 'all') {
        delete this.getParams.district
      }
      this.currentIndex = null
      this.getList()
    },
    async clickBox(index, location_id) {
      try {
        this.currentIndex = index
        this.location_id = location_id
        const data = await cacheLocationDetail('get', null, { params: { location_id: location_id }})
        this.agvData = data || []
      } catch (e) {
        //
      }
    }
  }
}
</script>

<style lang="scss" scoped>
    // ::-webkit-scrollbar {
    //   width: 10px
    // }
    // ::-webkit-scrollbar-track{
    //   background-color:#f8f8f8;
    // }
    // ::-webkit-scrollbar-thumb{
    //   background-color:#dddddd;
    // }
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
      border-radius: 5%;
      width: 55px;
      height: 70px;
      display: inline-block;
      margin:8px 7px 0 0px;
      line-height: 20px;
      text-align: center;
      color: #fff;
      font-size: 14px;
      overflow: hidden;
    }
    .border-style{
        border:3px dashed #000;
        line-height: 20px;
    }
    .item {
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 10px;
  }
  .box-card{
    position: relative;
    width: 45%;
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
</style>
