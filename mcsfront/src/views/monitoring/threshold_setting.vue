<template>
  <div>
    <!-- 检测指标阈值设置 -->
    <div class="top-search-box">
      <el-button v-permission="['env_indicator','change']" type="primary" @click="addFun">保存</el-button>
    </div>
    <div v-loading="loading" class="center-box">
      <el-table :data="tableData" border style="width: 60%" stripe>
        <el-table-column label="指标点名称" prop="group_name" min-width="10">
          <template slot-scope="{row}">
            {{ indicatorName.find(d=>d.type === row.indicator_type).name }}
          </template>
        </el-table-column>
        <el-table-column label="告警阈值" prop="warning_value" min-width="10">
          <template slot-scope="{row}">
            <el-input v-model="row.warning_value" type="number" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="报警阈值" prop="alarm_value" min-width="10">
          <template slot-scope="{row}">
            <el-input v-model="row.alarm_value" type="number" size="small" />
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { envIndicators } from '@/api/base_w'
export default {
  name: 'ThresholdSetting',
  data() {
    return {
      tableData: [],
      loading: false,
      indicatorName: [
        { type: 1, name: '温度' },
        { type: 2, name: '湿度' },
        { type: 3, name: '0.3微米离子数' },
        { type: 4, name: '0.5微米离子数' },
        { type: 5, name: '1微米离子数' },
        { type: 6, name: '3微米离子数' },
        { type: 7, name: '5微米离子数' }
      ]
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        const data = await envIndicators('get', null, { params: {} })
        this.tableData = data

      } catch (e) {
        //
      }
    },
    async addFun() {
      try {
        this.tableData.forEach(d => {
          if (!d.alarm_value || !d.warning_value) {
            this.$message('需要全部填写完整')
            throw new Error("除数不能为零")
          }
        })
        await envIndicators('post', null, { data: this.tableData })
        this.$message.success('保存成功')
      } catch (e) {
        //
      }
    }
  },
}
</script>

<style lang="scss" scoped>

</style>