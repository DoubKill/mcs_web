<template>
  <div v-loading="loading">
    <!-- 数采信息监控 -->
    <div class="content-wrapper">
      <iframe id="ifra" ref="iframe" name="ifra" width="100%" :height="heightMy" src="" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataCapture',
  data() {
    return {
      loading: false,
      heightMy: document.body.clientHeight - 150 + 'px'
    }
  },
  mounted() {
    // this.src_ = 'http://10.20.180.152:9000/'
    const _this = this
    _this.loading = true
    this.src_ = 'http://10.10.120.40:6001/'
    this.$refs.iframe.src = this.src_
    const iframe = this.$refs.iframe
    var data = {
      'account': 'mes',
      'password': 123456,
      'version': '1.0.0'
    }
    if (iframe.attachEvent) { // 兼容浏览器判断
      iframe.attachEvent('onload', function() {
        _this.loading = false
        const iframeWin = iframe.contentWindow
        iframeWin.postMessage(JSON.stringify(data), _this.src_)
      })
    } else {
      iframe.onload = function() {
        _this.loading = false
        const iframeWin = iframe.contentWindow
        iframeWin.postMessage(JSON.stringify(data), _this.src_)
      }
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
