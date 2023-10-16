from django.urls import include, path
from rest_framework.routers import DefaultRouter

from basics.views import CommonCodeView, GlobalCodeTypeViewSet, GlobalCodeViewSet, \
    ProcessSectionViewSet, PlatFormInfoViewSet, RestLocationViewSet, RoutingSchemaViewSet, PlatformGroupViewSet, \
    CacheDeviceInfoViewSet, EmptyBasketRouteSchemaView, EquipLocationView, WorkAreaViewSet, GlobalSettingsView, \
    LocationViewSet, LocationGroupViewSet, ThresholdDisplayViewSet, CheckConfView, AgvTypeViewSet

router = DefaultRouter()

# 公共代码类型
router.register(r'global-types', GlobalCodeTypeViewSet)

# 公共代码
router.register(r'global-codes', GlobalCodeViewSet)

# AGV类型
router.register(r'agv-type', AgvTypeViewSet)

# 工作区
router.register(r'work-areas', WorkAreaViewSet)

# 工艺段配置
router.register(r'process-sections', ProcessSectionViewSet)

# 工艺站台配置
router.register(r'platform-info', PlatFormInfoViewSet)

# 堆栈配置
router.register(r'cache-device-info', CacheDeviceInfoViewSet)

# 缓存/休息停靠位
router.register(r'rest-locations', RestLocationViewSet)  # 已弃用

# 休息位
router.register(r'locations', LocationViewSet)

# 缓存/休息停靠位
router.register(r'location-groups', LocationGroupViewSet)

# 站台定线
router.register(r'routing-schema', RoutingSchemaViewSet)

# 设备组
router.register(r'platform-group', PlatformGroupViewSet)

# 分流显示
router.register(r'threshold-display', ThresholdDisplayViewSet)

urlpatterns = [
    path('common-code/', CommonCodeView.as_view()),  # 获取默认的c
    path('empty-routing-schema/', EmptyBasketRouteSchemaView.as_view()),
    path('equip-locations/', EquipLocationView.as_view()),
    path('global-settings/', GlobalSettingsView.as_view()),  # 全局配置
    path('check-conf/', CheckConfView.as_view()),
    path('', include(router.urls)),
]
