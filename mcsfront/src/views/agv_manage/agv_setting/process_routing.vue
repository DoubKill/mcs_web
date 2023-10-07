<template>
  <div class="process-road-new">
    <!--新 工艺路线 -->
    <div v-loading="loading">
      <div v-for="(itemKey,val) in bottomCardData" :key="val" class="topCard">
        <div class="topOne">{{ val }}</div>
        <div class="bottomOne">进料类型</div>
        <div class="bottomTwo">出料类型</div>
      </div>
      <div style="flex: 1;">
        <div v-for="(item,key,index) in bottomCardData" :key="index" class="bottomCard">
          <div class="leftOne">
            <div
              v-for="(item1,index1) in item.in"
              :key="index1"
              :style="{'background':materialTypelist.find(d=>d.port_material_type_name===item1.material_type)?materialTypelist.find(d=>d.port_material_type_name===item1.material_type).color:'' }"
              class="smallBox"
              :title="item1.platform_name"
            >{{ item1.platform_name }}
            </div>
          </div>
          <div class="rightOne">
            <div
              v-for="(item1,index1) in item.out"
              :key="index1"
              :style="{'background':materialTypelist.find(d=>d.port_material_type_name===item1.material_type)?materialTypelist.find(d=>d.port_material_type_name===item1.material_type).color:'' }"
              class="smallBox"
              :title="item1.platform_name"
            >
              <span style="">{{ item1.platform_name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { processRoute } from '@/api/base_w'
export default {
  name: 'ProcessRouting',
  data() {
    return {
      topCardData: [],
      bottomCardData: [],
      loading: false,
      materialTypelist: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await processRoute('get', null, {})
        this.bottomCardData = data.data || {}
        this.materialTypelist = data.material_types
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .process-road-new{
    display: flex;
    background: #F0F1F5;
    height: 90vh;
    overflow-x: auto;
    white-space: nowrap;
    padding-left:10px;
   .el-divider--horizontal{
      margin-left: 20px;
    }
   .topCard{
    color: #000;
    display:inline-block;
    .topOne{
      border-radius: 0.3rem;
      background: #FFFFFF;
      margin-left: 10px;
      margin-right: 20px;
      text-align: center;
      margin-top: 20px;
      border-style:solid;
      border-color: #A0C9F1;
      border-width:1px;
      line-height: 40px;
      width: 180px;
      height: 40px;
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
      width: 85px;
      height: 40px;
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
