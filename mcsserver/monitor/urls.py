from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from monitor.views import TaskMonitorViewSet, InventoryInProcessMonitorView, ErrorWarningMonitorView, \
#     BasketTransportMonitorView, CacheLocationMonitorView, CacheLocationDetailMonitorView, AGVMonitorView, \
#     AGVDetailMonitorView, PlatformMonitorView, PlatformDetailMonitorView, AGVTaskMonitorView, OrderHistoryView, \
#     CacheStationMonitorView, CacheStationDetailMonitorView
from monitor.views import TaskMonitorViewSet, CacheStationMonitorView, CacheStationDetailMonitorView, AGVMonitorView, \
    AGVDetailMonitorView, EquipStatusMonitorView, OrderHistoryView, RealTimeView, InProcessView, AGVPackageMonitorView, AgvInProcessView, InProcessTrendView, \
    AlarmView, QTimeReportView, TaskDurationReportView

router = DefaultRouter()

router.register('task-monitor', TaskMonitorViewSet)  # 任务监控

urlpatterns = [
    path('', include(router.urls)),
    #
    # # 在制库存监控
    # path('inventory-in-process/', InventoryInProcessMonitorView.as_view()),
    #
    # # 异常预警监控
    # path('error-warning/', ErrorWarningMonitorView.as_view()),
    #
    # # 花篮RFID追溯
    # path('basket-transport/', BasketTransportMonitorView.as_view()),
    #
    # # 缓存位监控
    # path('cache-location/', CacheLocationMonitorView.as_view()),
    # # 缓存位详情监控
    # path('cache-location-detail/', CacheLocationDetailMonitorView.as_view()),
    #
    # agv状态监控
    path('agv/', AGVMonitorView.as_view()),
    # agv详情监控
    path('agv-detail/', AGVDetailMonitorView.as_view()),
    # AGV包号查询
    path('agv-package/', AGVPackageMonitorView.as_view()),

    # # 站台监控
    # path('platform/', PlatformMonitorView.as_view()),
    # # 站台详情监控
    # path('platform-detail/', PlatformDetailMonitorView.as_view()),
    #
    # 缓存站监控
    path('cache-station/', CacheStationMonitorView.as_view()),
    # 缓存站详情监控
    path('cache-station-detail/', CacheStationDetailMonitorView.as_view()),
    path('equip-status/', EquipStatusMonitorView.as_view()),

    # # agv状态监控列表
    # path('agv-task/', AGVTaskMonitorView.as_view()),
    #
    # 历史任务查询
    path('order-history/', OrderHistoryView.as_view()),
    # 实时监控
    path('real-time-monitor/', RealTimeView.as_view()),
    # 在制产能汇总
    path('in-process-monitor/', InProcessView.as_view()),
    # AGV实时在制
    path('agv-in-process/', AgvInProcessView.as_view()),
    # 在制趋势
    path('in-process-trend/', InProcessTrendView.as_view()),
    # 告警
    path('alarm/', AlarmView.as_view()),
    # QTime占比报表
    path('qtime-report/', QTimeReportView.as_view()),
    # 任务时长统计报表
    path('task-duration-report/', TaskDurationReportView.as_view()),
]
