<template>
  <div v-loading="loading">
    <!-- 异常预警监控 -->
    <div
      v-for="(item, key) in warnList"
      :key="key"
      style="display:inline-block;margin-left:10px;margin-top: 20px;"
    >
      <div
        :style="{'background':colorList[key-1],'color':'#FFF','width':'50px','height':'5px','display':'inline-block'}"
      />
      <div style="display:inline-block;color: #5E585A;margin-left: 5px">{{ item }}</div>
    </div>
    <br>
    <div
      v-for="(item,index) in boxData"
      :key="index"
      :class="['box-style']"
      :style="{'background':colorList[item.warning_type-1]}"
    >{{ item.message }}</div>
  </div>
</template>

<script>
import { abnormalMonitor } from '@/api/jqy'
export default {
  name: 'AbnormalMonitor',
  data() {
    return {
      colorList: ['#F1F1F1', '#DCDBDA', '#C4C5CA', '#E2E1D6', '#DDE1E4', '#E9D6B8', '#E2DFDE', '#F0D7B1'],
      getParams: {},
      boxData: [],
      warnList: {}
    }
  },
  watch: {
    $route: {
      handler() {
        if (this.$route.fullPath === '/abnormal-monitor') {
          this.getList()
          this._setInterval = setInterval(d => {
            this.getList()
          }, 5000)
        } else {
          window.clearInterval(this._setInterval)
        }
      },
      deep: true, // 深度监听
      immediate: true // 第一次初始化渲染就可以监听到
    }
  },
  created() {
    // this.getList()
  },
  destroyed() {
    window.clearInterval(this._setInterval)
  },
  methods: {
    async getList() {
      try {
        this.loading = true
        const data = await abnormalMonitor('get', null, { params: this.getParams })
        this.warnList = data.warning_types || []
        this.boxData = data.data || []
        this.loading = false
      } catch (e) {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
    .box-style{
        width: 260px;
        height: 120px;
        display: inline-block;
        margin:10px 10px 0 10px;
        line-height: 40px;
        padding-left:5px;
        color: #000;
        font-size: 18px;
        overflow: hidden;
    }
</style>
