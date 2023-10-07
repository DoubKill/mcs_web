<template>
  <div>
    <!-- AGV每日产能统计 -->
    <div class="top-search-box">
      <div style="height: 40px;line-height: 40px;display: flex;float:left">
        <div style="font-size: 20px;font-weight:800;">产能报表</div>
        <div>( 统计单位：片 )</div>
      </div>
      <el-form :inline="true" style="float:right">
        <el-form-item label="查询时间">
          <el-date-picker
            v-model="dateValue"
            size="small"
            type="datetimerange"
            :clearable="false"
            value-format="yyyy-MM-dd HH:mm:ss"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            @change="changeDate"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="success"
            icon="el-icon-search"
            size="small"
            @click="changeList"
          >搜索</el-button>
          <el-button
            v-permission="['agv_capacity_statistics','export']"
            type="blue"
            icon="el-icon-download"
            size="small"
            :loading="btnExportLoad"
            @click="exportFun"
          >导出</el-button>
        </el-form-item>
      </el-form>
      <div style="clear:both" />
    </div>
    <div
      v-loading="loading"
      class="center-box"
    >
      <el-table
        id="out-table"
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        :span-method="objectSpanMethod"
        style="width: 100%"
        stripe
      >
        <el-table-column
          prop="process_name"
          label="工序"
          min-width="20"
        />
        <el-table-column
          prop="equip_name"
          label="线别"
          min-width="20"
        />
        <el-table-column
          prop="full_up"
          label="上满料"
          min-width="20"
        />
        <el-table-column
          prop="full_down"
          label="取满料"
          min-width="20"
        />
        <el-table-column
          prop="empty_up"
          label="上空花篮"
          min-width="20"
        />
        <el-table-column
          prop="empty_down"
          label="取空花篮"
          min-width="20"
        />
        <el-table-column
          prop="full_up_total"
          label="上满料汇总"
          min-width="20"
        />
        <el-table-column
          prop="full_down_total"
          label="取满料汇总"
          min-width="20"
        />
        <el-table-column
          prop="empty_up_total"
          label="上空花篮汇总"
          min-width="20"
        />
        <el-table-column
          prop="empty_down_total"
          label="取空花篮汇总"
          min-width="20"
        />
      </el-table>
    </div>
  </div>
</template>

<script lang="js">
import { agvCapacityStatistics } from '@/api/jqy'
import { setDate, exportExcel } from '@/utils'
export default {
  name: 'CapacityStatistics',
  components: {},
  data() {
    return {
      dateValue: [setDate() + ' 00:00:00', setDate() + ' 23:59:59'],
      tableData: [],
      total: 0,
      btnExportLoad: false,
      getParams: {},
      btnLoading: false,
      loading: true
    }
  },
  created() {
    this.getParams.st = setDate() + ' 00:00:00'
    this.getParams.et = setDate() + ' 23:59:59'
    this.getList()
  },
  mounted() {
  },
  methods: {
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if ([0, 6, 7, 8, 9].includes(columnIndex) && this.spanArr) {
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
    },
    async getList() {
      try {
        this.loading = true
        const data = await agvCapacityStatistics('get', null, { params: this.getParams })
        this.tableData = data || []
        this.loading = false
        this.spanArr = []
        this.pos = null
        for (var i = 0; i < this.tableData.length; i++) {
          if (i === 0) {
            // 如果是第一条记录（即索引是0的时候），向数组中加入１
            this.spanArr.push(1)
            this.pos = 0
          } else {
            if (this.tableData[i].process_name === this.tableData[i - 1].process_name) {
              // 如果a相等就累加，并且push 0  这里是根据一样的a匹配
              this.spanArr[this.pos] += 1
              this.spanArr.push(0)
            } else {
              // 不相等push 1
              this.spanArr.push(1)
              this.pos = i
            }
          }
        }
      } catch (e) {
        this.loading = false
      }
    },
    changeDate(arr) {
      this.getParams.st = arr ? arr[0] : ''
      this.getParams.et = arr ? arr[1] : ''
    },
    exportFun() {
      exportExcel('AGV每日产能统计')
    },
    changeList() {
      this.getList()
    }
  }
}
</script>

<style lang="scss" scoped>

</style>

