<template>
  <div id="app">
    <router-view />
    <el-backtop target="#app" />
  </div>
</template>

<script>
export default {
  name: 'App'
  // mounted() {
  // document.getElementById('app').onclick = function(val) {
  // }
  // }
}
</script>
