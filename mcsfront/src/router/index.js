import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
// import { equipRoutes } from './index_equip'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [{
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [{
      path: '/redirect/:path(.*)',
      component: () => import('@/views/redirect/index')
    }]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/translate/real-time',
    component: () => import('@/views/report_data/real_time'),
    hidden: true,
    meta: {
      isPhone: true // 走不走登录和全限
    }
  }
  // {
  //   path: '/phone/fault-day-statistics',
  //   component: () => import('@/views/quality_management/phone/fault-day-statistics'),
  //   hidden: true,
  //   meta: {
  //     isPhone: true // 走不走登录和全限
  //   }
  // },
]
// 存在权限的路由
// meta.permissionName  权限
export const asyncRoutes = [{
    path: '/home',
    component: Layout,
    redirect: '/homePage',
    name: 'home',
    meta: {
      title: 'documentation',
      icon: 'el-icon-s-home'
    },
    children: [{
        path: '/homePage',
        component: () => import('@/views/home/index'),
        name: 'HomePageMain',
        meta: {
          title: '首页',
          icon: 'el-icon-s-home'
        }
      },
      {
        path: '/user-setting',
        redirect: '/user-manage',
        component: () => import('@/views/user_manage/a-index'),
        name: 'UserManageIndex',
        meta: {
          title: '系统管理',
          icon: 'el-icon-setting'
        },
        children: [{
            path: '/user-manage',
            component: () => import('@/views/user_manage/index'),
            name: 'UserManage',
            meta: {
              faName: 'UserManageIndex',
              title: '用户管理',
              permissionName: 'users'
            }
          },
          {
            path: '/group-manage',
            component: () => import('@/views/user_manage/group_manage'),
            name: 'GroupManage',
            meta: {
              faName: 'UserManageIndex',
              title: '角色管理',
              permissionName: 'roles'
            }
          },
          {
            path: '/personnel-framework',
            component: () => import('@/views/user_manage/personnel_framework'),
            name: 'PersonnelFramework',
            meta: {
              faName: 'UserManageIndex',
              title: '人员组织架构',
              permissionName: 'department'
            }
          },
          {
            path: '/edit-log-query',
            component: () => import('@/views/report_manage/edit_log_query'),
            name: 'EditLogQuery',
            meta: {
              faName: 'UserManageIndex',
              title: '操作履历',
              permissionName: 'operation_log'
            }
          }
        ]
      },
      // {
      //   path: '/cockpit-manage',
      //   redirect: '/data-board',
      //   component: () => import('@/views/cockpit_manage/a-index'),
      //   name: 'CockpitManage',
      //   meta: {
      //     title: '驾驶舱管理',
      //     icon: 'el-icon-s-data'
      //   },
      //   children: [
      //     {
      //       path: '/data-board',
      //       component: () => import('@/views/cockpit_manage/data_board'),
      //       name: 'DataBoard',
      //       meta: {
      //         faName: 'CockpitManage',
      //         title: '数据看板',
      //         permissionName: 'data_board'
      //       }
      //     },
      //     {
      //       path: '/statistical-version',
      //       component: () => import('@/views/statistical_manage/statistical_version'),
      //       name: 'StatisticalVersion',
      //       meta: {
      //         faName: 'CockpitManage',
      //         title: '统计看板',
      //         permissionName: 'task_capacity_analysis'
      //       }
      //     }
      //   ] },
      // {
      //   path: '/system-manage',
      //   component: () => import('@/views/system_manage/a-index'),
      //   redirect: '/code-manage',
      //   name: 'SystemManage',
      //   meta: {
      //     title: '系统管理',
      //     icon: 'el-icon-setting'
      //   },
      //   children: [{
      //     path: '/code-manage',
      //     component: () => import('@/views/system_manage/code_manage'),
      //     name: 'CodeManage',
      //     meta: {
      //       title: '公用代码管理'
      //     }
      //   }]
      // },
      {
        path: '/agv-base',
        redirect: '/device-manage',
        component: () => import('@/views/agv_manage/agv_base/a-index'),
        name: 'AgvBase',
        meta: {
          title: '基础信息管理',
          icon: 'el-icon-document'
        },
        children: [{
            path: '/global-setting',
            component: () => import('@/views/system_manage/global_setting'),
            name: 'GlobalSetting',
            meta: {
              faName: 'AgvBase',
              title: '全局配置',
              permissionName: 'global_conf'
            }
          },
          {
            path: '/rack-type',
            component: () => import('@/views/agv_manage/agv_base/rack_type'),
            name: 'RackType',
            meta: {
              faName: 'AgvBase',
              title: 'AGV类型管理',
              permissionName: 'agv_type'
            }
          },
          {
            path: '/workspace-manage',
            component: () => import('@/views/system_manage/workspace_manage'),
            name: 'WorkspaceManage',
            meta: {
              faName: 'AgvBase',
              title: '工作区管理',
              permissionName: 'work_area'
            }
          },
          // {
          //   path: '/code-manage',
          //   component: () => import('@/views/system_manage/code_manage'),
          //   name: 'CodeManage',
          //   meta: {
          //     faName: 'AgvBase',
          //     title: '公共代码管理',
          //     permissionName: 'global_types'
          //   }
          // },
          {
            path: '/process-setting',
            name: 'ProcessSetting',
            component: () => import('@/views/agv_manage/agv_base/process_setting'),
            meta: {
              faName: 'AgvBase',
              title: '工艺段配置',
              permissionName: 'process'
            }
          },
          {
            path: '/rest-manage',
            component: () => import('@/views/system_manage/rest_manage'),
            name: 'RestManage',
            meta: {
              faName: 'AgvBase',
              title: '休息位管理',
              permissionName: 'locations'
            }
          },
          {
            path: '/rest-group-manage',
            component: () => import('@/views/system_manage/rest_group_manage'),
            name: 'RestGroupManage',
            meta: {
              faName: 'AgvBase',
              title: '休息位组管理',
              permissionName: 'location_groups'
            }
          },
          {
            path: '/process-station-setting',
            name: 'ProcessStationSetting',
            component: () => import('@/views/agv_manage/agv_base/process_station_setting'),
            meta: {
              faName: 'AgvBase',
              title: '工艺站台配置',
              permissionName: 'stations'
            }
          },
          {
            path: '/exit-platform-setting',
            name: 'ExitPlatformSetting',
            component: () => import('@/views/set_alignment/exit_platform_setting'),
            meta: {
              faName: 'AgvBase',
              title: '堆栈站台配置',
              permissionName: 'caches'
            }
          },
          {
            path: '/configuration-check',
            name: 'ConfigurationCheck',
            component: () => import('@/views/set_alignment/configuration_check'),
            meta: {
              faName: 'AgvBase',
              title: '配置检查',
              permissionName: 'check_conf'
            }
          }
          // {
          //   path: '/docking-space',
          //   component: () => import('@/views/set_alignment/docking_space'),
          //   name: 'DockingSpace',
          //   meta: {
          //     faName: 'AgvBase',
          //     title: '缓存停靠位配置',
          //     permissionName: ''
          //   }
          // }
        ]
      },
      {
        path: '/set-alignment',
        component: () => import('@/views/set_alignment/a-index'),
        redirect: '/inventory-query',
        name: 'SetAlignment',
        meta: {
          title: '设置定线',
          icon: 'el-icon-document-checked'
        },
        children: [{
            path: '/alignment-query',
            component: () => import('@/views/set_alignment/alignment_query'),
            name: 'AlignmentQuery',
            meta: {
              faName: 'SetAlignment',
              title: '定线管理',
              permissionName: 'schemas'
            }
          },
          {
            path: '/basket-alignment',
            component: () => import('@/views/set_alignment/basket_alignment'),
            name: 'basket-alignment',
            meta: {
              faName: 'SetAlignment',
              title: '空花篮定线',
              permissionName: 'empty_schemas'
            }
          },
          {
            path: '/device-group-settings',
            component: () => import('@/views/set_alignment/device_group_settings'),
            name: 'DeviceGroupSettings',
            meta: {
              faName: 'SetAlignment',
              title: '设备组设置',
              permissionName: 'dev_groups'
            }
          }
        ]
      },
      // {
      //   path: '/report-manage',
      //   redirect: '/task-query',
      //   component: () => import('@/views/report_manage/a-index'),
      //   name: 'ReportManage',
      //   meta: {
      //     title: '报表管理',
      //     icon: 'el-icon-data-analysis'
      //   },
      //   children: [
      //     {
      //       path: '/edit-log-query',
      //       component: () => import('@/views/report_manage/edit_log_query'),
      //       name: 'EditLogQuery',
      //       meta: {
      //         faName: 'ReportManage',
      //         title: '操作日志查询',
      //         permissionName: 'user_operation_log'
      //       }
      //     }
      //   ]
      // },
      // {
      //   path: '/task-manage',
      //   component: () => import('@/views/task_manage/a-index'),
      //   redirect: '/task-cache',
      //   name: 'TaskManage',
      //   meta: {
      //     title: '任务管理',
      //     icon: 'el-icon-document-checked'
      //   },
      //   children: [
      //     {
      //       path: '/task-cache',
      //       component: () => import('@/views/task_manage/task_cache'),
      //       name: 'task_cache',
      //       meta: {
      //         faName: 'TaskManage',
      //         title: '缓存站任务管理',
      //         permissionName: 'cache_station_tasks'
      //       }
      //     }
      //   ]
      // },
      {
        path: '/equip-monitor',
        component: () => import('@/views/equip_monitor/a-index'),
        redirect: '/feeding-machine',
        name: 'EquipMonitor',
        meta: {
          title: '设备监控',
          icon: 'el-icon-view'
        },
        children: [{
            path: '/task-monitor',
            component: () => import('@/views/equip_monitor/task_monitor'),
            name: 'TaskMonitor',
            meta: {
              faName: 'EquipMonitor',
              title: '任务监控',
              permissionName: 'tasks'
            }
          },
          {
            path: '/agv-monitor',
            component: () => import('@/views/equip_monitor/agv_monitor'),
            name: 'AgvMonitor',
            meta: {
              faName: 'EquipMonitor',
              title: 'AGV状态监控',
              permissionName: 'agv_state'
            }
          },
          {
            path: '/material-monitor',
            component: () => import('@/views/equip_monitor/monitor/material_monitor'),
            name: 'material_monitor',
            meta: {
              faName: 'EquipMonitor',
              title: 'AGV物料监控',
              permissionName: 'agv_package'
            }
          },
          {
            path: '/real-monitor',
            component: () => import('@/views/equip_monitor/real_monitor'),
            name: 'RealMonitor',
            meta: {
              faName: 'EquipMonitor',
              title: '站台实时监控',
              permissionName: 'real_state'
            }
          },
          {
            path: '/platform-status',
            component: () => import('@/views/equip_monitor/monitor/platform_status'),
            name: 'PlatformStatus',
            meta: {
              faName: 'EquipMonitor',
              title: '站台状态监控',
              permissionName: 'station_state'
            }
          },
          {
            path: '/cache-station-monitor',
            component: () => import('@/views/equip_monitor/cache_station_monitor'),
            name: 'CacheStationMonitor',
            meta: {
              faName: 'EquipMonitor',
              title: '堆栈状态监控',
              permissionName: 'cache_state'
            }
          },
          {
            path: '/real-time',
            component: () => import('@/views/report_data/real_time'),
            name: 'RealTime',
            meta: {
              faName: 'EquipMonitor',
              title: '在制产能汇总',
              permissionName: 'zz_state'
            }
          }
          // {
          //   path: '/stock-monitor',
          //   component: () => import('@/views/equip_monitor/stock_monitor'),
          //   name: 'StockMonitor',
          //   meta: {
          //     faName: 'EquipMonitor',
          //     title: '在制库存监控',
          //     permissionName: 'inventory_in_process'
          //   }
          // },
          // {
          //   path: '/realtime-monitor',
          //   component: () => import('@/views/equip_monitor/monitor/realtime_monitor'),
          //   name: 'RealtimeMonitor',
          //   meta: {
          //     faName: 'EquipMonitor',
          //     title: '实时运行',
          //     permissionName: ''
          //   }
          // },
          // {
          //   path: '/data-capture',
          //   component: () => import('@/views/equip_monitor/data_capture'),
          //   name: 'DataCapture',
          //   meta: {
          //     faName: 'EquipMonitor',
          //     title: '数采信息监控',
          //     permissionName: 'device_monitor'
          //   }
          // }
        ]
      },
      {
        path: '/report-data',
        component: () => import('@/views/report_data/a-index'),
        redirect: '/task-query',
        name: 'ReportData',
        meta: {
          title: '报表数据',
          icon: 'el-icon-s-data'
        },
        children: [{
            path: '/task-query',
            component: () => import('@/views/report_manage/task_query'),
            name: 'TaskQuery',
            meta: {
              faName: 'ReportManage',
              title: '历史任务查询',
              permissionName: 'history_tasks'
            }
          },
          {
            path: '/process-capacity',
            component: () => import('@/views/report_data/process_capacity'),
            name: 'ProcessCapacity',
            meta: {
              faName: 'ReportManage',
              title: '工序产能报表',
              permissionName: 'product_static'
            }
          },
          {
            path: '/diversion-display',
            component: () => import('@/views/report_data/diversion_display'),
            name: 'DiversionDisplay',
            meta: {
              faName: 'ReportManage',
              title: '分流展示',
              permissionName: 'threshold_display'
            }
          },
          {
            path: '/process-trend',
            component: () => import('@/views/report_data/process_trend'),
            name: 'ProcessTrend',
            meta: {
              faName: 'ReportData',
              title: '在制趋势',
              permissionName: 'in_process_trend'
            }
          },
          {
            path: '/AGV-real',
            component: () => import('@/views/report_data/AGV_real'),
            name: 'AGVReal',
            meta: {
              faName: 'ReportData',
              title: 'AGV实时在制',
              permissionName: 'agv_in_process'
            }
          },
          {
            path: '/QTime-forms',
            component: () => import('@/views/report_data/QTime_forms'),
            name: 'QTimeForms',
            meta: {
              faName: 'ReportData',
              title: '堆栈超时料报表',
              permissionName: 'qtime_report'
            }
          },
          {
            path: '/station-date-back',
            component: () => import('@/views/report_data/station_date_back'),
            name: 'StationDateBack',
            meta: {
              faName: 'ReportData',
              title: '站台任务追溯报表',
              permissionName: 'station_track'
            }
          },
          {
            path: '/task-duration',
            component: () => import('@/views/report_data/task_duration'),
            name: 'TaskDuration',
            meta: {
              faName: 'ReportData',
              title: '任务时长统计报表',
              permissionName: 'task_duration_report'
            }
          }
        ]
      },
      {
        path: '/environmental-monitoring',
        component: () => import('@/views/monitoring/a-index'),
        redirect: '/threshold-setting',
        name: 'EnvironmentalMonitoring',
        meta: {
          title: '环境监测',
          icon: 'el-icon-s-data'
        },
        children: [{
          path: '/threshold-setting',
          component: () => import('@/views/monitoring/threshold_setting'),
          name: 'ThresholdSetting',
          meta: {
            faName: 'EnvironmentalMonitoring',
            title: '检测指标阈值设置',
            permissionName: 'env_indicator'
          }
        }, {
          path: '/detection-point',
          component: () => import('@/views/monitoring/detection_point'),
          name: 'DetectionPoint',
          meta: {
            faName: 'EnvironmentalMonitoring',
            title: '检测点配置',
            permissionName: 'env_location'
          }
        }, {
          path: '/detection-task',
          component: () => import('@/views/monitoring/detection_task'),
          name: 'DetectionTask',
          meta: {
            faName: 'EnvironmentalMonitoring',
            title: '检测任务配置',
            permissionName: 'env_task'
          }
        }, {
          path: '/report-forms',
          component: () => import('@/views/monitoring/report_forms'),
          name: 'ReportForms',
          meta: {
            faName: 'EnvironmentalMonitoring',
            title: '检测报表',
            permissionName: 'env_check_history'
          }
        }]
      },
      {
        path: '/alarm-log-data',
        component: () => import('@/views/report_data/alarm-log-a-index'),
        redirect: '/alarm-log',
        name: 'AlarmLogData',
        meta: {
          title: '告警记录',
          icon: 'el-icon-s-check'
        },
        children: [{
          path: '/alarm-log',
          component: () => import('@/views/report_data/alarm_log'),
          name: 'AlarmLog',
          meta: {
            faName: 'ReportData',
            title: '告警记录',
            permissionName: 'alarm'
          }
        }]
      }
    ]
  },
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]
// asyncRoutes = asyncRoutes.concat(equipRoutes)

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({
    y: 0
  }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
