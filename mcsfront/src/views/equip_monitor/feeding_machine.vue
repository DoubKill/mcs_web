<template>
  <div class="feeding_machine">
    <!-- 发料机上料预测 -->
    <div class="top-search-box">
      <el-form :inline="true">
        <el-form-item label="设备编号">
          <el-input v-model="getParams.a" size="small" clearable placeholder="设备编号" />
        </el-form-item>
        <el-form-item label="设备名称">
          <el-input v-model="getParams.area_code" size="small" clearable placeholder="设备名称" />
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" size="small" @click="getList">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-row :gutter="12" class="center-box">
      <el-col :span="8">
        <el-card shadow="always">
          <div class="title-style one" />
          总是显示
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="always">
          <div class="title-style two" />
          总是显示
        </el-card>
      </el-col>
      <el-col :span="8" style="margin-top:12px">
        <el-card shadow="always">
          <div class="title-style three" />
          总是显示
        </el-card>
      </el-col>
      <el-col :span="16" style="margin-top:12px">
        <el-card shadow="always">
          <div class="title-style four" />
          总是显示
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'FeedingMachine',
  data() {
    return {
      getParams: {}
    }
  },
  methods: {
    async getList() {
      try {
        // this.loading = true
        // const data = await restArea('get', null, { params: this.getParams })
        // this.tableData = data.results || []
        // this.total = data.count
        // this.loading = false
      } catch (e) {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss">
    .feeding_machine{
        .el-card{
            height: 300px;
            // overflow-y: scroll;

        }
        ::-webkit-scrollbar {/*滚动条整体样式*/
            width:4px;/*高宽分别对应横竖滚动条的尺寸*/
            height:4px;
        }
        ::-webkit-scrollbar-thumb {/*滚动条里面小方块*/
            border-radius:5px;
            -webkit-box-shadow: inset005pxrgba(0,0,0,0.2);
            background:rgba(0,0,0,0.2);
        }
        .el-card__body{
            padding:0 !important;
        }
        .title-style{
            height: 40px;
            line-height: 40px;
            background: rgb(129, 176, 227);
            position: relative;
            &::after{
                content: '制绒设备当前花篮数量';
                position: absolute;
                vertical-align: middle;
                top: 4px;
                left: 8px;
                background: transparent;
                border: 1px solid #fff;
                width: 96%;
                height: 80%;
                line-height: 30px;
                color: #fff;
                padding-left:10px;
            }
        }
        .two{
            background: rgb(243, 153, 74);
            &::after{
                content: 'MES所在任务计划';
                width: 98%;
            }
        }
        .three{
            background: rgb(112, 201, 161);
            &::after{
                content: '制绒设备AGV花篮数量统计';
            }
        }
        .four{
            background: rgb(75, 114, 159);
            &::after{
                content: 'MES当前最新任务数量';
                width: 98%;
            }
        }
    }
</style>
