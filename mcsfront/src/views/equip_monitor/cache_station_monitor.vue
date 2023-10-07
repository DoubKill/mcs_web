<template>
  <div>
    <!-- 堆栈状态监控 -->
    <div class="top-search-box" style="padding:3px 16px">
      <el-form :inline="true">
        <!-- <el-form-item label="状态">
          <el-select
            v-model="getParams.is_used"
            size="small"
            placeholder="请选择状态"
            clearable
            @change="clickTabs"
          >
            <el-option
              v-for="user in [{value:1,label:'已使用'},{value:0,label:'已禁用'}]"
              :key="user.value"
              :label="user.label"
              :value="user.value"
            />
          </el-select>
        </el-form-item> -->
        <el-form-item>
          <el-button type="success" icon="el-icon-refresh" size="small" @click="changeList">刷新</el-button>
        </el-form-item>
        <el-form-item style="float:right;">
          <span style="margin-left:20px">总库位数：{{ total_locations }}</span>
          <span style="margin-left:20px">已使用库位：{{ used_location }}</span>
          <span style="margin-left:20px">花篮总数：{{ total_basket_num }}</span>
        </el-form-item>
      </el-form>
    </div>
    <el-row :gutter="10">
      <el-col :span="8">
        <div>
          <div class="w-tabs-style" style="width:100%;max-height:80vh;overflow-y:scroll;">
            <div v-for="(item, index) in leftData" :key="index" style="margin-bottom:3px !important">
              <el-card :key="item.id" :class="[currentIndex===item.id?'border-style':'','box-card1']" @click.native="clickBox(item.id)">
                <el-divider content-position="left"><span :style="{'color':item.overtime_flag?'red':''}">{{ item.equip_name }}</span></el-divider>
                <el-row :gutter="10">
                  <el-col :span="12">
                    <div class="text item">
                      <div style="width:50%;display: inline-block;">
                        <span class="weightSet">
                          进料状态
                        </span>
                        <el-button style="vertical-align: middle;" :type="item.in_is_used?'success':'danger'" size="mini">
                        </el-button>
                      </div>
                      <div style="width:50%;display: inline-block;">
                        <span class="weightSet">
                          出料状态
                        </span>
                        <el-button style="vertical-align: middle;" :type="item.out_is_used?'success':'danger'" size="mini">
                        </el-button>
                      </div>

                    </div>
                    <div class="text item">
                      <div style="width:50%;display: inline-block;">
                        <span class="weightSet">
                          规格
                        </span>
                        {{ item.specification }}
                      </div>
                      <div style="width:50%;display: inline-block;">
                        <span class="weightSet">
                          库存(篮)
                        </span>
                        {{ item.basket_num }}
                      </div>
                    </div>
                  </el-col>
                  <el-col :span="5" style="text-align: center;">
                    <el-progress style="white-space: pre-wrap;" type="circle" :percentage="item.overtime_storage_location?item.overtime_storage_location/item.used_storage_location*100:0" :format="format1(item.overtime_storage_location,item.used_storage_location)" :width="90" />
                  </el-col>
                  <el-col :span="5" style="text-align: center;">
                    <el-progress style="white-space: pre-wrap;" type="circle" :percentage="item.used_storage_location/item.total_storage_location*100" :format="format(item.used_storage_location,item.total_storage_location)" :width="90" />
                  </el-col>
                </el-row>
              </el-card>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="grid-content bg-purple" style="max-height: 80vh;overflow-y:auto">
          <el-card v-for="(val, key, index) in rightData" :key="index" style="margin-top: 10px">
            <el-divider content-position="left">{{ rightData.length-key+'层' }}</el-divider>
            <div v-for="(val1, key1, index1) in val" :key="index1" style="margin-bottom:3px !important">
              <el-tooltip v-for="(item1,index2) in val1" :key="index2" :open-delay="500" placement="top">
                <div slot="content">库位编号:{{ item1.equip_code+'_'+item1.row+'_'+item1.column+'_'+item1.layer }}<br>库位物料:{{ item1.material_type }}<br>花篮数量:{{ item1.basket_num }}<br>QTime(秒):{{ item1.q_time }}<br>下料时间:{{ item1.trans_time }}</div>
                <el-card :body-style="{ padding: '0px' }" class="box-card" :style="{'margin-bottom':'3px !important','width':(100-3*val1.length)/val1.length +'%'}">
                  <div slot="header" class="clearfix">
                    <!-- <span :style="{'color':item1.overtime_flag?'red':''}">{{ item1.equip_code+'_'+item1.row+'_'+item1.column+'_'+item1.layer+'【' +item1.basket_num+'】' }}</span> -->
                    <span :style="{'color':item1.overtime_flag?'red':''}">{{ item1.material_type?item1.material_type:'-' }}</span>
                    <el-progress :show-text="false" status="success" :percentage="item1.basket_num/item1.storage_num*100" />
                  </div>
                </el-card>
              </el-tooltip>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { cacheStation, cacheStationDetail } from '@/api/jqy'
export default {
  name: 'CacheStationMonitor',
  data() {
    return {
      getParams: {},
      all_tasks: 0,
      leftData: [],
      rightData: [],
      obj: null,
      total_locations: 0,
      used_location: 0,
      total_basket_num: 0,
      currentIndex: null
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/cache-station-monitor') {
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
            if (this.obj) {
              this.clickBox(this.obj)
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
  },
  methods: {
    changeList() {
      if (this.currentIndex !== null) {
        this.clickBox(this.obj)
      }
      this.getList()
    },
    format(val, val2) {
      return () => {
        return '库位使用比\n' + val + '/' + val2
      }
    },
    format1(val, val2) {
      return () => {
        return '超时料占比\n' + (val || 0) + '/' + val2
      }
    },
    clickTabs() {
      this.currentIndex = null
      this.rightData = []
      this.getList()
    },
    async getList() {
      try {
        this.loading = true
        const data = await cacheStation('get', null, { params: this.getParams })
        this.total_locations = data.total_locations
        this.used_location = data.used_location
        this.total_basket_num = data.total_basket_num
        this.leftData = data.data || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    async clickBox(item) {
      this.currentIndex = item
      this.obj = item
      try {
        const data = await cacheStationDetail('get', null, { params: { equip_id: item } })
        this.rightData = data.data || []
        this.rightData = Object.keys(data.data).sort((a, b) => {
          return b - a
          // 为了以防万一，这里先排好键值顺序，代码省略，也可以直接用sort()默认排序
        }).map((v) => {
          return data.data[v] // 根据原键名从obj中再找对应的项
        })
      } catch (e) {
        //
      }
    }
  }
}
</script>

  <style lang="scss" scoped>
      .el-card ::v-deep .el-card__header {
          padding: 10px 20px !important;
       }
      .w-tabs-style{
          margin-left:1%;
          display: inline-block;
      }
      .el-tag--dark{
          cursor: pointer;
      }
      .box-style{
          width: 160px;
          height: 40px;
          display: inline-block;
          margin:8px 2px 0 3px;
          line-height: 40px;
          padding-left:5px;
          color: #fff;
          font-size: 18px;
          overflow: hidden;
      }
      .border-style{
          background: #E2F2EF;
      }
      .item {
      margin-top: 10px;
      margin-bottom: 10px;
      margin-left: 10px;
    }
    .weightSet{
        font-weight: 700;
    }
    .box-card{
      font-size:16px;
      position: relative;
      width: 47%;
      display: inline-block;
    }
    .box-card1{
      margin-top: 5px;
      position: relative;
      width: 100%;
      // display: inline-block;
    }
  </style>
