<template>
  <div
    v-loading="loading"
    class="transferLimit"
  >
    <h3 v-if="!sectionId && !groupId" style="color:red">请选择部门</h3>
    <el-button
      v-if="isExport"
      type="primary"
      @click="exportTable"
    >导出Excel</el-button>
    <el-table
      v-if="permissionsData.length>0"
      id="out-table"
      :data="permissionsData"
      style="width: 100%;"
      border
      row-key="id"
      :span-method="objectSpanMethod"
    >
      <el-table-column
        prop="category_name"
        label="模块"
        width="100"
      />
      <el-table-column
        prop="name"
        label="菜单"
        width="180"
      />
      <el-table-column label="权限">
        <template slot="header" slot-scope="scope">
          权限
          <el-checkbox
            v-if="!exportBool"
            v-model="checkAll"
            style="margin-left:20px"
            @change="checkAllChange"
          >全选</el-checkbox>
          <span v-if="false">{{ scope }}</span>
        </template>
        <template slot-scope="scope">
          <el-checkbox
            v-if="!exportBool"
            v-model="scope.row.checkAll"
            @change="handleCheckAllChange($event,scope.row,scope.row.permissions)"
          >全选</el-checkbox>
          <div style="margin: 15px 0;" />
          <el-checkbox-group
            v-model="scope.row.checkedCities"
            @change="handleCheckedCitiesChange($event,scope.row)"
          >
            <el-checkbox
              v-for="(itemData,_i) in scope.row.permissions"
              :key="itemData.id"
              :label="itemData.id"
            >{{ itemData.name }}
              <span v-if="exportBool&&scope.row.permissions.length!==_i+1">、</span>
            </el-checkbox>
          </el-checkbox-group>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { permissions } from '@/api/permission'
import { exportExcel } from '@/utils/index'
export default {
  props: {
    defaultPermissions: {
      type: Array,
      default: () => {
        return []
      }
    },
    groupId: {
      type: Number,
      default: 0
    },
    menu: {
      type: [Number, String],
      default: ''
    },
    category: { // 主菜单
      type: [Number, String],
      default: ''
    },
    isExport: { // 主菜单
      type: Boolean,
      default: false
    },
    sectionId: {
      type: [Number, String],
      default: ''
    },
    viewSectionPermission: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      permissionsData: [],
      loading: false,
      checkAll: false,
      permissionsDataAll: [],
      exportBool: false,
      spanArr: [],
      pos: null
    }
  },
  computed: {
  },
  watch: {
    groupId() {
      this.permissionsData.forEach(data => { // 查看角色
        data.permissions.forEach(D => {
          D.checkedCities = []
        })
        data.checkAll = false
      })
      this.getPermissions()
    },
    sectionId() {
      this.permissionsData.forEach(data => {
        data.permissions.forEach(D => {
          D.checkedCities = []
        })
        data.checkAll = false
      })
      if (!this.groupId) {
        this.getPermissions()
      }
    },
    menu(val) {
      this.checkAll = false
      if (val) {
        this.permissionsData = this.permissionsDataAll.filter(item => {
          return item.name.toLowerCase()
            .indexOf(val.toLowerCase()) > -1
        })
      } else {
        this.permissionsData = this.permissionsDataAll
      }
    },
    category(val) {
      this.checkAll = false
      if (val) {
        this.permissionsData = this.permissionsDataAll.filter(item => {
          return item.category_name.toLowerCase()
            .indexOf(val.toLowerCase()) > -1
        })
      } else {
        this.permissionsData = this.permissionsDataAll
      }
    }
  },
  mounted() {
    this.getPermissions()
  },
  methods: {
    getPermissions() {
      this.permissionsData = []
      if (!this.sectionId && !this.groupId) {
        return
      }
      this.loading = true
      let obj = {}
      if (this.sectionId) {
        obj.section_id = this.sectionId
      } else {
        delete obj.section_id
      }
      if (this.viewSectionPermission) {
        obj.view_section_permission = 1
      } else {
        delete obj.view_section_permission
      }
      if (this.groupId) {
        obj = { group_id: this.groupId }
      }
      this.loading = true
      permissions('get', null, { params: obj }).then(response => {
        const permissionsArr = response.result || []
        this.permissionsData = permissionsArr
        this.permissionsList = permissionsArr

        this.spanArr = []
        this.pos = null
        this.permissionsData.forEach((data, i) => {
          const arr = []
          data.permissions.forEach(D => {
            if (this.defaultPermissions && this.defaultPermissions.length) {
              this.defaultPermissions.forEach(dd => {
                if (D.id === dd) {
                  D.has_permission = true
                  arr.push(D.id)
                }
              })
            } else {
              if (D.has_permission) {
                arr.push(D.id)
              }
            }
          })
          if (data.permissions.length === arr.length) {
            this.$set(data, 'checkAll', true)
          } else {
            this.$set(data, 'checkAll', false)
          }
          this.$set(data, 'checkedCities', arr)

          if (i === 0) {
            // 如果是第一条记录（即索引是0的时候），向数组中加入１
            this.spanArr.push(1)
            this.pos = 0
          } else {
            if (this.permissionsData[i].category_name === this.permissionsData[i - 1].category_name) {
              // 如果a相等就累加，并且push 0  这里是根据一样的a匹配
              this.spanArr[this.pos] += 1
              this.spanArr.push(0)
            } else {
              // 不相等push 1
              this.spanArr.push(1)
              this.pos = i
            }
          }
        })

        this.permissionsDataAll = this.permissionsData
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    handleCheckAllChange(val, row, permissionsList) {
      const arr = []
      permissionsList.forEach(D => {
        arr.push(D.id)
      })
      if (val) {
        row.checkedCities = arr
      } else {
        row.checkedCities = []
      }
      this.setPermissionsData()
    },
    handleCheckedCitiesChange(data, row) {
      const checkedCount = data.length
      row.checkAll = checkedCount === row.permissions.length
      this.setPermissionsData()
    },
    setPermissionsData(permissionsData) {
      const arr = []
      this.permissionsList.forEach(Data => {
        arr.push(...Data.checkedCities)
      })
      this.$emit('changeTransferPermissions', arr)
    },
    checkAllChange(bool) {
      this.permissionsData.forEach(data => {
        const arr = []
        data.permissions.forEach(D => {
          D.has_permission = bool
          if (D.has_permission) {
            arr.push(D.id)
          }
        })
        if (data.permissions.length === arr.length) {
          this.$set(data, 'checkAll', true)
        } else {
          this.$set(data, 'checkAll', false)
        }
        this.$set(data, 'checkedCities', arr)
      })

      this.setPermissionsData()
    },
    exportTable() {
      this.exportBool = true
      setTimeout(d => {
        exportExcel('权限')
        this.exportBool = false
      }, 300)
    },
    objectSpanMethod({ row, column, rowIndex, columnIndex }) {
      if ([0].includes(columnIndex) && this.spanArr) {
        const _row = this.spanArr[rowIndex]
        const _col = _row > 0 ? 1 : 0
        return {
          rowspan: _row,
          colspan: _col
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.transferLimit{
  max-height: 500px;
  overflow-y: scroll;
}
</style>
