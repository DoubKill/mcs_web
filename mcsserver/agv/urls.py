from django.urls import include, path
from rest_framework.routers import DefaultRouter

from agv.views import RCSOrderTracebackView, ProductivityStatisticsView, StationTaskTrackView, EnvIndicatorsView, \
    EnvCheckLocationsViewSet, EnvCheckTasksViewSet, EnvLocationCheckHistoryView, EnvCheckResultTraceback

router = DefaultRouter()

router.register(r'env-check-locations', EnvCheckLocationsViewSet)
router.register(r'env-check-tasks', EnvCheckTasksViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rcs-order-traceback/', RCSOrderTracebackView.as_view()),
    path('product-static/', ProductivityStatisticsView.as_view()),
    path('station-task-track/', StationTaskTrackView.as_view()),
    path('env-indicators/', EnvIndicatorsView.as_view()),
    path('env-location-check-history/', EnvLocationCheckHistoryView.as_view()),
    path('env-check-traceback/', EnvCheckResultTraceback.as_view()),
]
