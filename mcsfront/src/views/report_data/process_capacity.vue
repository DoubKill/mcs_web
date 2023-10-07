<template>
  <div class="real_monitor">
    <!-- 工序产能报表 -->
    <div v-loading="loading" class="center-box">
      <div class="botton-box">
        <el-form inline>
          <el-form-item label="传篮时间">
            <el-date-picker v-model="dateValue" size="small" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" value-format="yyyy-MM-dd HH:mm:ss" @change="changeDate" />
          </el-form-item>
          <el-form-item>
            <!-- v-permission="['cache_device_conf','export']" -->
            <el-button type="blue" icon="el-icon-download" size="small" :loading="exportLoading" @click="exportFun">导出</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-table id="out-table" :data="tableData" tooltip-effect="dark" style="width: 100%" stripe>
        <el-table-column label="工艺段名称" prop="process_name" sortable />
        <el-table-column label="送花蓝产量" prop="in_basket_num" sortable />
        <el-table-column label="接花蓝产量" prop="out_basket_num" sortable />
      </el-table>
    </div>
  </div>
</template>

<script lang="js">
// import common from '@/utils/common'
import { setDate, exportExcel } from '@/utils/index'
import { productStatic } from '@/api/jqy'
export default {
  name: 'ProcessCapacity',
  components: {},
  data() {
    return {
      dateValue: [],
      tableData: [],
      btnExportLoad: false,
      getParams: {},
      loading: true,
      exportLoading: false
    }
  },
  created() {
    this.dateValue = [setDate() + ' 00:00:00', setDate() + getTime()]
    this.getParams.st = setDate() + ' 00:00:00'
    this.getParams.et = setDate() + getTime()
    this.getList()
  },
  mounted() {
  },
  methods: {
    changeDate(arr) {
      this.getParams.st = arr ? arr[0] : ''
      this.getParams.et = arr ? arr[1] : ''
      this.getList()
    },
    async getList() {
      try {
        this.loading = true
        const data = await productStatic('get', null, { params: this.getParams })
        this.tableData = data.data || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    },
    changeList() {
      this.getList()
    },
    exportFun() {
      this.exportLoading = true
      setTimeout(d => {
        exportExcel('工序产能报表')
        this.exportLoading = false
      }, 300)
    },
  }
}
function getTime() {
  var date = new Date()
  var hour = date.getHours() // 时
  var minutes = date.getMinutes() // 分
  var seconds = date.getSeconds() // 秒
  // 给一位数的数据前面加 “0”
  if (hour >= 0 && hour <= 9) {
    hour = '0' + hour
  }
  if (minutes >= 0 && minutes <= 9) {
    minutes = '0' + minutes
  }
  if (seconds >= 0 && seconds <= 9) {
    seconds = '0' + seconds
  }
  return ' ' + hour + ':' + minutes + ':' + seconds
}
</script>

<style lang="scss" scoped>
  .el-tooltip__popper{
    max-width:50%
  }
</style>

