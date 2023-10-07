<template>
  <div class="basket_alignment">
    <!-- 空花篮定线 -->
    <el-tabs v-model="tabCurrent" class="w-tabs-style" @tab-click="handleClick">
      <el-tab-pane v-for="(item) in tabHearder" :key="item.id" :label="item.name" :name="item.id" />
    </el-tabs>
    <el-form :inline="true" class="top-search-box" v-if="tabCurrent!=='1'">
      <el-form-item label="工艺段">
        <el-select v-model="getParams.process_id" size="small" placeholder="请选择" filterable @visible-change="visibleChange" @change="changeList">
          <el-option v-for="item in process_section_list" :key="item.id" :label="item.process_name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item style="float:right;">
        <el-button type="success" icon="el-icon-getParams" size="small" @click="SaveFun" v-permission="['empty_schemas','change']">保 存</el-button>
        <!-- <el-button v-permission="['basket_transport','export']" type="blue" size="small" @click="enableFun">启 用</el-button> -->
      </el-form-item>
    </el-form>

    <div v-for="(item,i) in tableData" :key="i">
      <el-table class="center-box" stripe :data="item" style="width: 100%">
        <el-table-column :label="i?'堆栈名称':'站台名称'" prop="instance_name" width="100" />
        <el-table-column label="下料花篮类型" prop="up_basket_type" width="120" />
        <el-table-column label="定线">
          <template slot-scope="{row,$index}">
            <el-checkbox-group v-model="row.routing_plats" style="margin-right:20px;display:inline-block;vertical-align: middle;">
              <el-checkbox-button v-for="city in alignmentAll" :key="city.instance_id" :label="city.instance_id">{{ city.name }}</el-checkbox-button>
            </el-checkbox-group>

            <el-checkbox-group v-model="row.route_caches" fill="rgb(76 162 104)" style="margin-right:20px;display:inline-block;vertical-align: middle;">
              <el-checkbox-button v-for="city in alignmentAll1" :key="city.instance_id" :label="city.instance_id">{{ city.name }}</el-checkbox-button>
            </el-checkbox-group>

            <el-checkbox-group v-model="row.route_locations" fill="#b54eaa" style="margin-right:20px;display:inline-block;vertical-align: middle;">
              <el-checkbox-button v-for="city in alignmentAll2" :key="city.instance_id" :label="city.instance_id">{{ city.name }}</el-checkbox-button>
            </el-checkbox-group>
            <el-button style="vertical-align: middle;" size="small" @click="checkAllFun(row.checkAll,$index,i)">{{ row.checkAll?'反选': '全选' }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div v-if="tableData.length===0" style="text-align:center;margin-top:20px">暂无数据</div>
  </div>
</template>

<script>
import { emptyRoutingSchema } from '@/api/base_w'
import { processSections } from '@/api/jqy'
export default {
  name: 'BasketAlignment',
  data() {
    return {
      tabCurrent: '2',
      tabHearder: [{ id: '2', name: '预定线' }], // { id: '1', name: '当前定线' },
      getParams: {},
      tableData: [],
      alignmentAll: [],
      alignmentAll1: [],
      alignmentAll2: [],
      alignmentAllId: [],
      alignmentAllId1: [],
      alignmentAllId2: [],
      process_section_list: []
    }
  },
  created() {
    this.getProcessSectionList()
  },
  methods: {
    async getList() {
      try {
        this.tableData = []
        const data = await emptyRoutingSchema('get', null, { params: this.getParams })
        let arr = []
        let arr1 = []
        data.data.forEach(d => {
          if (d.dp_type === 2) {
            arr1.push(d)
          } else {
            arr.push(d)
          }
        })
        this.tableData = [arr, arr1]
        this.alignmentAll = data.all_routing_plts || []
        this.alignmentAll1 = data.all_cache_devices || []
        this.alignmentAll2 = data.all_rest_locations || []

        this.alignmentAllId = []
        this.alignmentAllId1 = []
        this.alignmentAllId2 = []
        this.alignmentAll.forEach(d => {
          this.alignmentAllId.push(d.instance_id)
        })
        this.alignmentAll1.forEach(d => {
          this.alignmentAllId1.push(d.instance_id)
        })
        this.alignmentAll2.forEach(d => {
          this.alignmentAllId2.push(d.instance_id)
        })
      } catch (e) {
        //
      }
    },
    handleClick() {

    },
    changeList() {
      this.getList()
    },
    async SaveFun() {
      try {
        let arr = [...this.tableData[0], ...this.tableData[1]]
        let _obj = { "process_id": this.getParams.process_id, "plt_date": arr }
        await emptyRoutingSchema('post', null, { data: _obj })
        this.$store.dispatch('settings/operateTypeSetting', '保存操作')
        this.$message.success('保存成功')
      } catch (e) {
        //
      }
    },
    enableFun() { },
    checkAllFun(e, index, faIndex) {
      this.tableData[faIndex][index].checkAll = !e

      if (this.tableData[faIndex][index].checkAll) {
        this.tableData[faIndex][index].routing_plats = this.alignmentAllId
        this.tableData[faIndex][index].route_caches = this.alignmentAllId1
        this.tableData[faIndex][index].route_locations = this.alignmentAllId2
      } else {
        this.tableData[faIndex][index].routing_plats = []
        this.tableData[faIndex][index].route_caches = []
        this.tableData[faIndex][index].route_locations = []
      }
    },
    visibleChange(bool) {
      if (bool) {
        this.getProcessSectionList()
      }
    },
    async getProcessSectionList() {
      try {
        const data = await processSections('get', null, { params: { all: 1, out_empty_flat: 1 } })
        this.process_section_list = data || []
        if (!this.getParams.process_id) {
          this.getParams.process_id = data.length > 0 ? data[0].id : ''
          this.getList()
        }
      } catch (e) {
        //
      }
    }
  }
}
</script>

<style lang="scss">
    .basket_alignment{.w-tabs-style{
        margin-left:15px;
    }
    .el-table__body-wrapper{
      height: auto !important;
    }
  }
</style>
