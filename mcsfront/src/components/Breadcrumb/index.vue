<template>
  <el-breadcrumb class="app-breadcrumb" separator="/">
    <div v-if="levelList.length>0">
      <transition-group name="breadcrumb">
        <el-breadcrumb-item v-for="(item,index) in levelList" :key="item?item.name:index">
          <span v-if="item&&item.redirect==='noRedirect'||index==levelList.length-1" class="no-redirect">{{ generateTitle(item?item.meta.title:'') }}</span>
          <a v-else @click.prevent="handleLink(item)">{{ generateTitle(item?item.meta.title:'') }}</a>
        </el-breadcrumb-item>
      </transition-group>
    </div>
  </el-breadcrumb>
</template>

<script>
import pathToRegexp from 'path-to-regexp'
import { generateTitle } from '@/utils/i18n'

export default {
  data() {
    return {
      levelList: null
    }
  },
  watch: {
    $route() {
      this.getBreadcrumb()
    }
  },
  created() {
    this.getBreadcrumb()
  },
  methods: {
    generateTitle,
    getBreadcrumb() {
      // only show routes with meta.title
      const matched = this.$route.matched.filter(item => item.meta && item.meta.title)
      // const first = matched[0]

      // if (!this.isDashboard(first)) {
      // matched = [{ path: '/dashboard', meta: { title: '首页' }}].concat(matched)
      // }

      // this.levelList = matched.filter(item => item.meta && item.meta.title && item.meta.breadcrumb !== false)
      // console.log(this.levelList, 'this.levelList')

      const levelList = matched.filter(item => item.meta && item.meta.title && item.meta.breadcrumb !== false)
      // console.log(levelList, 'levelList')

      // if (_length > 1 && levelList[0].meta.title === levelList[_length - 1].meta.title) {
      //   this.levelList = [levelList[0]]
      //   return
      // }
      const a = levelList.filter(d => d.name !== 'home')
      this.levelList = a
    },
    isDashboard(route) {
      const path = route && route.meta.icon
      if (!path) {
        return false
      }
      return path.trim().toLocaleLowerCase() === 'Dashboard'.toLocaleLowerCase()
    },
    pathCompile(path) {
      // To solve this problem https://github.com/PanJiaChen/vue-element-admin/issues/561
      const { params } = this.$route
      var toPath = pathToRegexp.compile(path)
      return toPath(params)
    },
    handleLink(item) {
      const { redirect, path } = item
      console.log(redirect, 'redirect')
      if (redirect) {
        this.$router.push(redirect)
        return
      }
      this.$router.push(this.pathCompile(path))
    }
  }
}
</script>

<style lang="scss" scoped>
.app-breadcrumb.el-breadcrumb {
  display: inline-block;
  font-size: 14px;
  line-height: 42px;
  margin-left: 8px;
  .el-breadcrumb__inner{
    // a {
    //   color:red;
    //   &:hover {
    //   color: rgb(11, 58, 189);
    // }
    // }
  }

  .no-redirect {
    color: #fff;
    cursor: text;
  }
}
</style>
