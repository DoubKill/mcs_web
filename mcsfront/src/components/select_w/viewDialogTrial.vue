<template>
  <div>
    <!-- 试验方法详情 -->
    <el-dialog
      title=""
      :visible.sync="dialogVisible"
      width="80%"
      :before-close="handleClose"
    >
      <div v-loading="loading">
        <el-form :inline="true">
          <el-form-item style="margin-right:50px" :label="showData.type_name" />
          <el-form-item label="胶料编码:">
            {{ showData.material_no }}
          </el-form-item>
          <el-form-item v-if="testMethodSelectShow" label="试验方法:">
            <testMethodSelect :create-load="true" :test-type-id="showData.test_type_id" :testmodeprop="testMode" @changeSelect="testMethodChange" />
          </el-form-item>
        </el-form>
        <el-table
          :data="tableData"
          border
          :span-method="objectSpanMethod"
        >
          <el-table-column
            prop="level"
            label="等级"
          />
          <el-table-column
            prop="result"
            label="处理意见"
          />
          <el-table-column
            :key="0"
            prop="limits_val"
            label="区分"
          />
          <el-table-column
            v-for="(itemChild,i) in headTable"
            :key="i+1"
            :label="itemChild.name"
          >
            <template slot-scope="scope">
              <span v-if="scope.row.limits_val === '上限'">
                {{ scope.row[itemChild.name]?scope.row[itemChild.name].upper_limit:'' }}
              </span>
              <span v-else>
                {{ scope.row[itemChild.name]?scope.row[itemChild.name].lower_limit:'' }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import testMethodSelect from '@/components/select_w/testMethodSelect'
import { matIndicatorTab, materialDataPoints } from '@/api/base_w'
import { deepClone } from '@/utils/index'
export default {
  components: { testMethodSelect },
  props: {
    show: Boolean,
    showData: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {
      dialogVisible: false,
      testMode: '',
      search: this.showData,
      loading: true,
      testMethodSelectShow: false,
      tableData: [],
      headTable: []
    }
  },
  watch: {
    show(val) {
      this.dialogVisible = val
      if (val) {
        this.testMethodSelectShow = true
        this.search = this.showData
      }
    }
  },
  methods: {
    async getList() {
      try {
        const data = await matIndicatorTab('get', null, { params: this.search })
        const arr = []
        data.forEach((D, i) => {
          D.limits_val = '上限'
          arr.push(D)
          const a = deepClone(D)
          a.limits_val = '下限'
          arr.push(a)
        })
        return arr
      } catch (e) {
        this.loading = false
      }
    },
    async getTestTypes() {
      try {
        const data = await materialDataPoints('get', null, { params: this.search })
        return data
      } catch (e) {
        this.loading = false
      }
    },
    handleClose(done) {
      this.$emit('handleClose', false)
      this.testMethodSelectShow = false
      done()
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 0 || columnIndex === 1) {
        if (rowIndex % 2 === 0) {
          return {
            rowspan: 2,
            colspan: 1
          }
        } else {
          return {
            rowspan: 0,
            colspan: 0
          }
        }
      }
    },
    testMethodChange(val) {
      this.search.test_method_id = val
      Promise.all([this.getList(), this.getTestTypes()]).then((data) => {
        this.tableData = data[0]
        this.headTable = data[1]
        this.loading = false
      }).catch((e) => {
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
