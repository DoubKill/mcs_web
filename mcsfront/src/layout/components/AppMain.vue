<template>
  <section class="app-main">
    <!-- <transition name="fade-transform" mode="out-in"> -->
    <div v-if="key === '/homePage'||key === '/exit-platform-setting'">
      <router-view :key="key" />
    </div>
    <keep-alive v-else :include="cachedViews">
      <router-view :key="key" />
    </keep-alive>
    <!-- </transition> -->
  </section>
</template>

<script>
export default {
  name: 'AppMain',
  computed: {
    cachedViews() {
      return this.$store.state.tagsView.cachedViews
    },
    key() {
      return this.$route.path
    }
  }
}
</script>

<style scoped>
.box-card{
  margin: 10px;
}
.app-main {
  /*50 = navbar  */
  /* min-height: calc(100vh - 200px); */
  width: 100%;
  position: relative;
  overflow: hidden;
}
.fixed-header+.app-main {
  /* padding-top: 200px; */
}
</style>

<style lang="scss">
// fix css style bug in open el-dialog
.el-popup-parent--hidden {
  .fixed-header {
    padding-right: 15px;
  }
}
.app-main .el-card{
    border: none !important;
}
.app-main .box-card{
    margin: 14px !important;
    margin-top: 2px !important;
    .el-card__body{
      padding: 0 !important;
    }
}
</style>
