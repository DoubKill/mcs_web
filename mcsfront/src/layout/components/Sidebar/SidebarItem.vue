<template>
  <div v-if="!item.hidden">
    <!-- <template v-if="hasOneShowingChild(item.children,item) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)&&!item.alwaysShow">
      <app-link v-if="onlyOneChild.meta" :to="resolvePath(onlyOneChild.path)">
        <el-menu-item :index="resolvePath(onlyOneChild.path)" :class="{'submenu-title-noDropdown':!isNest}">
          <item :icon="onlyOneChild.meta.icon||(item.meta&&item.meta.icon)" :title="onlyOneChild.meta.title" />
        </el-menu-item>
      </app-link>
    </template> -->

    <!-- <el-submenu v-else ref="subMenu" :index="resolvePath(item.path)" popper-append-to-body>
      <template slot="title">
        <item v-if="item.meta" :icon="item.meta && item.meta.icon" :title="item.meta.title" />
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :is-nest="true"
        :item="child"
        :base-path="resolvePath(child.path)"
        class="nest-menu"
      />
    </el-submenu> -->
    <template v-if="hasOneShowingChild(item.children,item) && (!item.children||item.noShowingChildren)&&!item.alwaysShow&&!item.meta.icon">
      <app-link :to="item.path">
        <el-menu-item :index="item.path" :class="{'submenu-title-noDropdown':!isNest}">
          <item :icon="item.meta.icon||(item.meta&&item.meta.icon)" :title="generateTitle(item.meta.title)" />
        </el-menu-item>
      </app-link>
    </template>
    <el-submenu v-else-if="!item.meta.icon" ref="subMenu" :index="item.path" popper-append-to-body>
      <template slot="title">
        <item v-if="item.meta" :icon="item.meta && item.meta.icon" :title="generateTitle(item.meta.title)" />
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :is-nest="true"
        :item="child"
        :base-path="child.path"
        class="nest-menu"
      />
    </el-submenu>
    <div v-else>
      <div v-for="(itemC,i) in item.children" :key="i">
        <template v-if="hasOneShowingChild(itemC.children,itemC) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)&&!itemC.alwaysShow">
          <app-link v-if="onlyOneChild.meta" :to="onlyOneChild.path">
            <el-menu-item :index="onlyOneChild.path" :class="{'submenu-title-noDropdown':!isNest}">
              <item :icon="onlyOneChild.meta.icon||(onlyOneChild.meta&&itemC.meta.icon)" :title="generateTitle(onlyOneChild.meta.title)" />
            </el-menu-item>
          </app-link>
        </template>

        <el-submenu v-else ref="subMenu" :index="itemC.path" popper-append-to-body>
          <template slot="title">
            <item v-if="itemC.meta" :icon="itemC.meta && itemC.meta.icon" :title="generateTitle(itemC.meta.title)" />
          </template>
          <sidebar-item
            v-for="child in itemC.children"
            :key="child.path"
            :is-nest="true"
            :item="child"
            :base-path="child.path"
            class="nest-menu"
          />
        </el-submenu>
      </div>
    </div>

  </div>
</template>

<script>
// import path from 'path'
// import { isExternal } from '@/utils/validate'
import Item from './Item'
import AppLink from './Link'
import FixiOSBug from './FixiOSBug'
import { generateTitle } from '@/utils/i18n'

export default {
  name: 'SidebarItem',
  components: { Item, AppLink },
  mixins: [FixiOSBug],
  props: {
    // route object
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  data() {
    // To fix https://github.com/PanJiaChen/vue-admin-template/issues/237
    // TODO: refactor with render function
    this.onlyOneChild = null
    return {}
  },
  created() {
  },
  methods: {
    generateTitle,
    hasOneShowingChild(children = [], parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false
        } else {
          // Temp set(will be used if only has one showing child)
          this.onlyOneChild = item
          return true
        }
      })
      // When there is only one child router, the child router is displayed by default
      if (showingChildren.length === 1) {
        return true
      }

      // Show parent if there are no child router to display
      if (showingChildren.length === 0) {
        // this.onlyOneChild = { ... parent, path: '', noShowingChildren: true }
        this.onlyOneChild = { ... parent, noShowingChildren: true }
        return true
      }

      return false
    },
    resolvePath(routePath) {
      // if (isExternal(routePath)) {
      //   return routePath
      // }
      // if (isExternal(this.basePath)) {
      //   return this.basePath
      // }
      // return path.resolve(this.basePath, routePath)
    }
  }
}
</script>
