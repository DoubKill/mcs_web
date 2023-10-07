<template>
  <!-- 胶料下拉框 -->
  <el-select
    v-model="productBatchingId"
    clearable
    filterable
    :loading="loading"
    @change="productBatchingChanged"
    @visible-change="visibleChange"
  >
    <el-option
      v-for="item in productBatchings"
      :key="item.id"
      :label="item.stage_product_batch_no"
      :value="item.id"
    />
  </el-select>
</template>

<script>
import { rubberMaterialUrl } from '@/api/base_w'
export default {
  props: {
    isStageProductbatchNoRemove: {
      type: Boolean,
      default: false
    },
    // 过滤出启用和弃用的胶料
    makeUseBatch: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      productBatchings: [],
      productBatchingId: '',
      productBatchingById: {},
      loading: true
    }
  },
  created() {
  },
  methods: {
    productBatchingChanged() {
      this.$emit('productBatchingChanged', this.productBatchingById[this.productBatchingId])
    },
    visibleChange(bool) {
      if (bool && this.productBatchings.length === 0) {
        this.getProductBatchings()
      }
    },
    getProductBatchings() {
      this.loading = true
      // eslint-disable-next-line object-curly-spacing
      rubberMaterialUrl('get', null, { params: { all: 1 } }).then(response => {
        let productBatchings = response.results
        productBatchings.forEach(productBatching => {
          this.productBatchingById[productBatching.id] = productBatching
        })
        if (this.makeUseBatch) {
          let arr = []
          arr = productBatchings.filter(D => D.used_type === 4 || D.used_type === 6)
          productBatchings = arr
        }
        if (this.isStageProductbatchNoRemove) {
          // 根据stage_product_batch_no去重
          var obj = {}
          var newArr = productBatchings.reduce((item, next) => {
            obj[next.stage_product_batch_no]
              ? ' '
              : (obj[next.stage_product_batch_no] = true && item.push(next))
            return item
          }, [])
          productBatchings = newArr || []
        }
        this.loading = false
        this.productBatchings = productBatchings
      })
    }
  }
  // USE_TYPE_CHOICE = (
  //       (1, '编辑'),
  //       (2, '提交'),
  //       (3, '校对'),
  //       (4, '启用'),
  //       (5, '驳回'),
  //       (6, '废弃')
  //   )
}
</script>
