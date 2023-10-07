<template>
  <!-- 炼胶机类型 -->
  <el-select
    :value="id"
    clearable
    placeholder="请选择"
    :size="isMini"
    :disabled="isDisabled"
    filterable
    @change="changeFun"
  >
    <el-option
      v-for="item in equipsCategories"
      :key="item.id"
      :label="item.category_name"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { equip_category_url } from '@/api/rubber_recipe_fun'
export default {
  model: {
    prop: 'id',
    event: 'change'
  },
  props: {
    id: {
      type: [Number, String],
      required: false,
      default: undefined
    },
    equipTypeName: {
      type: String,
      required: false,
      default: '密炼设备'
    },
    isMini: {
      type: String,
      default: ''
    },
    isDisabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      equipsCategories: []
    }
  },
  created() {
    this.getEquipsCategories()
  },
  methods: {
    async getEquipsCategories() {
      const response = await equip_category_url('get', {
        params: {
          all: 1,
          equip_type_name: this.equipTypeName
        }
      })
      this.equipsCategories = response.results
    },
    // visibleChange(visible) {
    //   if (visible) {
    //     this.getEquipsCategories()
    //   }
    // },
    changeFun(event) {
      const arr = this.equipsCategories.filter(D => D.id === event)
      this.$emit('changeFun', arr[0])
      this.$emit('change', event)
    }
  }
}
</script>
