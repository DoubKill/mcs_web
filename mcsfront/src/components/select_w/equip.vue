<template>
  <div style="display:inline-block">
    <!-- 机台下拉框 设备编码-->
    <el-select
      v-model="_equip_no"
      :clearable="!isCreated||isClear"
      placeholder="请选择机台"
      :multiple="isMultiple"
      :disabled="disabled"
      :multiple-limit="multipleLimit"
      @change="changeSearch"
      @visible-change="visibleChange"
    >
      <el-option
        v-for="item in machineList"
        :key="item.equip_no"
        :label="item.equip_no"
        :value="item.equip_no"
      />
    </el-select>
  </div>
</template>

<script>
import { equipUrl } from '@/api/base_w'
export default {
  props: {
    // eslint-disable-next-line vue/prop-name-casing
    equip_no_props: {
      type: [String, Array],
      default: null
    },
    isObj: {
      type: Boolean,
      default: false
    },
    isMultiple: {
      type: Boolean,
      default: false
    },
    // 在created里面加载，并默认选中第一个
    isCreated: {
      type: Boolean,
      default: false
    },
    isClear: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    // 设备类型
    equipType: {
      type: String,
      default: '密炼设备'
    },
    multipleLimit: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      machineList: []
    }
  },
  computed: {
    _equip_no: {
      get() {
        return this.equip_no_props || ''
      },
      set(equip_no) {
        this.$emit('update:equip_no_props', equip_no)
      }
    }
  },
  created() {
    if (this.isCreated) {
      this.getMachineList()
    }
  },
  methods: {
    getMachineList() {
      var _this = this
      equipUrl('get', { params: { all: 1, category_name: this.equipType }})
        .then(function(response) {
          _this.machineList = response.results || []
          if (_this.isCreated) {
            if (_this.$route.path === '/alone/material_base_info_manage/') {
              _this.changeSearch(_this.$route.query.equip)
              return
            }
            _this.changeSearch(_this.machineList[0].equip_no)
          }
        })
        .catch(function() { })
    },
    changeSearch(id) {
      if (this.isObj) {
        const obj = this.machineList.find(d => d.equip_no === id)
        this.$emit('changeSearch', obj)
        return
      }
      this._equip_no = id
      this.$emit('changeSearch', id)
    },
    visibleChange(bool) {
      if (bool && !this.isCreated) {
        this.getMachineList()
      }
    }
  }
}
</script>

<style>
</style>
