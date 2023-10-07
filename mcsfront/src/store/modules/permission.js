import {
  asyncRoutes,
  constantRoutes
} from '@/router'

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({
    commit,
    state
  }, permission) {
    return new Promise(resolve => {
      const permissionObj = permission
      const accessedRoutes = filterAsyncRoutesMy(asyncRoutes, permissionObj)
      // 添加的路由
      commit('SET_ROUTES', accessedRoutes)
      // 使用router.addRoutes传accessedRoutes过去相当于push
      // 使用options.routes传allRoutes过去相当于替换
      const allRoutes = constantRoutes.concat(accessedRoutes)

      resolve(allRoutes)
    })
  }
}

export function filterAsyncRoutesMy(routes, permission) {
  const res = []
  routes.forEach(route => {
    const tmp = {
      ...route
    }

    if (hasPermissionMy(permission, tmp)) {
      if (tmp.children) {
        // if (tmp.meta && tmp.meta.permissionName) {
        // const permissionVal = permission[tmp.meta.permissionName]
        tmp.children = filterAsyncRoutesMy(tmp.children, permission)
        // }
        //  else {
        //   tmp.children = filterAsyncRoutesMy(tmp.children, permission)
        // }
      }
      if (Object.prototype.hasOwnProperty.call(tmp, 'children') && tmp.children.length === 0) {
        return
      }
      res.push(tmp)
    }
  })
  return res
}

function hasPermissionMy(permission, route) {
  if (route.meta && route.meta.permissionName && permission) {
    const val = permission[route.meta.permissionName]
    let boolIndex = null
    // if (Object.prototype.toString.call(val) === '[object Object]') {
    //   // 是第一层
    //   boolIndex = val
    // } else {
    // 是第二层
    boolIndex = val && val.indexOf('view') > -1
    // }
    return boolIndex && JSON.stringify(val) !== '{}' && JSON.stringify(val) !== '[]'
  } else {
    return true
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
