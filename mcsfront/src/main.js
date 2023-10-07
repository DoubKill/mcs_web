import Vue from 'vue'

import { debounce } from '@/utils'
import echarts from 'echarts'
Vue.prototype.$echarts = echarts
import VCharts from 'v-charts'
Vue.use(VCharts)

// import { decoration10, decoration8, decoration6 } from '@jiaminghi/data-view' // 首页头部动画
// Vue.use(decoration10)
// Vue.use(decoration8)
// Vue.use(decoration6)

// 按需引入虚拟表格
import { UTable, UTableColumn } from 'umy-ui'
Vue.component(UTable.name, UTable)
Vue.component(UTableColumn.name, UTableColumn)

import '@/utils/filterPublic'
import '@/utils/directives/index.js'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/element-ui.scss'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'
import i18n from './lang'

import '@/icons' // icon
import '@/permission' // permission control

import 'default-passive-events'

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
// if (process.env.NODE_ENV === 'production') {
//   const { mockXHR } = require('../mock')
//   mockXHR()
// }

// set ElementUI lang to EN
// Vue.use(ElementUI, { locale })
// 如果想要中文版 element-ui，按如下方式声明
// Vue.use(ElementUI)
Vue.use(Element, {
  ElementUI: 'mini',
  i18n: (key, value) => i18n.t(key, value)
})

Vue.config.productionTip = false

Vue.prototype.$debounce = debounce

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: h => h(App)
})
