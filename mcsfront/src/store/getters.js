const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  permission: (state) => {
    if (state.user.permission && (typeof state.user.permission) === 'string') {
      return JSON.parse(state.user.permission)
    } else {
      return state.user.permission
    }
  },
  name_MCS: state => state.user.name_MCS,
  userId: state => state.user.userId,
  routes: state => state.permission.routes,
  addRoutes: state => state.permission.addRoutes,
  editionNo: state => state.user.editionNo,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  operateType: state => state.settings.operateType
}
// 获取vuex数据
// import { mapGetters } from "vuex";
// computed: {
//   ...mapGetters(["name"]),
// },
export default getters
