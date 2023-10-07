<template>
  <div>
    <!-- 全局配置 -->
    <div v-loading="loading" class="center-box" style="margin-top:10px">
      <!-- <div class="botton-box">
        <el-button type="blue" icon="el-icon-plus" size="small" @click="addFun">新增</el-button>
        <el-button type="danger" icon="el-icon-delete" size="small" @click="deleteFun">删除</el-button>
      </div> -->
      <el-table ref="multipleTable" :data="tableData" stripe style="width: 60%" @selection-change="handleSelectionChange">
        <!-- <el-table-column
          type="selection"
          width="40"
        /> -->
        <el-table-column label="属性名称" prop="desc">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.desc" prefix-icon="el-icon-search" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              {{ row.desc }}
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="属性值" prop="value">
          <el-table-column min-width="10">
            <template slot="header" slot-scope="scope">
              <el-input v-model="getParams.value" prefix-icon="el-icon-search" size="small" clearable @input="getList" />
            </template>
            <template slot-scope="{row}">
              <span v-if="row.type==='choices'">{{ row.choices[row.value] }}</span>
              <span v-else>
                {{ row.type==='bool'?row.value==='1'?'是':'否':row.value }}
              </span>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template slot-scope="{row,$index}">
            <el-button v-permission="['global_conf','change']" size="small" type="text" @click="editShow(row,$index)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog :title="(currentIndex.toString()?'编辑':'新建')" :visible.sync="dialogVisible" width="300" :before-close="handleClose">
      <el-form ref="ruleForm" :model="currentObj" :rules="rules" label-width="150px">
        <el-form-item label="属性名称" prop="desc">
          <el-input v-model="currentObj.desc" :disabled="currentIndex.toString()?true:false" size="small" />
        </el-form-item>
        <el-form-item label="属性值" prop="value" v-if="currentObj.type!=='json'">
          <el-input v-if="currentObj.type==='str'" v-model="currentObj.value" placeholder="请输入字符" size="small" />
          <el-input-number v-else-if="currentObj.type==='int'" v-model="currentObj.value" style="width:200px" placeholder="请输入整数" size="small" controls-position="right" :min="0" />
          <el-radio-group v-else-if="currentObj.type==='bool'" v-model="currentObj.value">
            <el-radio label="0">否</el-radio>
            <el-radio label="1">是</el-radio>
          </el-radio-group>
          <el-select v-else-if="currentObj.type==='choices'" v-model="currentObj.value" size="small" placeholder="请选择">
            <el-option v-for="(item,key) in currentObj.choices" :key="item" :label="item" :value="key" />
          </el-select>
        </el-form-item>
        <div v-if="currentObj.type==='json_date'">
          <el-form-item v-if="currentObj.value['早班']" label="早班" prop="value">
            <el-time-picker v-model="currentObj.value.早班[0]" value-format="HH:mm:ss" placeholder="开始时间" :clearable="false">
            </el-time-picker>
            <el-time-picker v-model="currentObj.value.早班[1]" value-format="HH:mm:ss" placeholder="结束时间" :clearable="false">
            </el-time-picker>
          </el-form-item>
          <el-form-item v-if="currentObj.value['中班']" label="中班" prop="value">
            <el-time-picker v-model="currentObj.value.中班[0]" value-format="HH:mm:ss" placeholder="开始时间" :clearable="false">
            </el-time-picker>
            <el-time-picker v-model="currentObj.value.中班[1]" value-format="HH:mm:ss" placeholder="结束时间" :clearable="false">
            </el-time-picker>
          </el-form-item>
          <el-form-item v-if="currentObj.value['晚班']" label="晚班" prop="value">
            <el-time-picker v-model="currentObj.value.晚班[0]" value-format="HH:mm:ss" placeholder="开始时间" :clearable="false">
            </el-time-picker>
            <el-time-picker v-model="currentObj.value.晚班[1]" value-format="HH:mm:ss" placeholder="结束时间" :clearable="false">
            </el-time-picker>
          </el-form-item>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose(false)">取 消</el-button>
        <el-button type="primary" :loading="btnLoading" @click="submitFun()">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { globalSettings } from '@/api/base_w'
export default {
  name: 'GlobalSetting',
  data() {
    return {
      tableData: [],
      loading: false,
      dialogVisible: false,
      currentVal: [],
      currentObj: {},
      getParams: {},
      rules: {
        desc: [
          { required: true, message: '请填写', trigger: 'blur' }
        ],
        value: [
          { required: true, message: '请填写', trigger: 'blur' }
        ]
      },
      btnLoading: false,
      currentIndex: ''
    }
  },
  created() {
    this.getList()
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        this.tableData = []
        const data = await globalSettings('get', null, { params: this.getParams })
        this.tableData = data || []
        this.loading = false

        this.tableData.forEach(d => {
          if (d.type === 'json_date') {
            d.value = JSON.parse(d.value)
            for (const key in d.value) {
              if (Object.hasOwnProperty.call(d.value, key)) {
                d.value[key] = d.value[key].split('-')
              }
            }
          }
        })
      } catch (e) {
        this.loading = false
      }
    },
    handleClose(done) {
      this.dialogVisible = false
      this.currentObj = {}
      this.$refs.ruleForm.resetFields()
      if (done) {
        done()
      }
    },
    handleSelectionChange(val) {
      this.currentVal = val || []
    },
    addFun() {
      this.currentIndex = ''
      this.dialogVisible = true
    },
    editShow(row, index) {
      this.currentObj = JSON.parse(JSON.stringify(row))
      this.currentIndex = index
      this.dialogVisible = true
    },
    deleteFun() {
      this.$confirm('此操作删除不可逆, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (!this.currentVal.length) {
          this.$message('请选择列表数据')
          return
        }
        this.resultFun(1)
      }).catch(() => {
      })
    },
    submitFun() {
      this.$refs.ruleForm.validate(async (valid) => {
        if (valid) {
          this.resultFun()
        } else {
          return false
        }
      })
    },
    async resultFun(type) {
      try {
        this.btnLoading = true
        const _api = 'post'
        const arr1 = JSON.parse(JSON.stringify(this.tableData))
        if (type) {
          // 进行的删除
          const arr = []
          this.currentVal.forEach(d => {
            arr.push(d.desc)
          })
          arr.forEach(d => {
            arr1.splice(arr1.findIndex(dd => dd.desc === d), 1)
          })
        } else {
          if (this.currentIndex.toString()) {
            // 编辑
            arr1[this.currentIndex] = this.currentObj
          } else {
            arr1.push(this.currentObj)
          }
        }
        const obj = {}
        arr1.forEach(d => {
          obj[d.key_name] = d
        })
        let obj1 = JSON.parse(JSON.stringify(this.currentObj))
        if (obj1.type === 'json_date') {
          for (const key in obj1.value) {
            if (Object.hasOwnProperty.call(obj1.value, key)) {
              obj1.value[key] = obj1.value[key].join('-')
            }
          }
          obj1.value = JSON.stringify(obj1.value)
        }
        await globalSettings(_api, null, { data: obj1 })
        this.$message.success('操作成功')
        this.handleClose(null)
        this.getList()
        this.btnLoading = false
        this.$store.dispatch('settings/operateTypeSetting', '变更')
      } catch (e) {
        this.btnLoading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
