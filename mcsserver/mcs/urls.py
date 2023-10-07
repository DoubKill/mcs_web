"""mcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve as static_serve
from mcs import settings
from openapi.views import LocationSearchView, RCSAgvSearchView, PlatformGroupSearchView, PlatformSearchView, \
    PlatformLastTimeSearchView, PlatformLocationSearch
from django.views import static as st


urlpatterns = [
    path('api/v1/agv/', include('agv.urls')),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/basics/', include('basics.urls')),
    path('api/v1/monitor/', include('monitor.urls')),
    # path('admin/', admin.site.urls),
    # RCS调用
    path('api/v1/basics/rest-location-search/', LocationSearchView.as_view()),
    path('api/mcs/monitor/agvs/', RCSAgvSearchView.as_view()),
    path('api/mcs/monitor/device-groups/', PlatformGroupSearchView.as_view()),
    path('api/mcs/monitor/stations/', PlatformSearchView.as_view()),
    path('api/v1/basics/station-pred-time-search/', PlatformLastTimeSearchView.as_view()),
    path('api/v1/basics/location-search/', PlatformLocationSearch.as_view()),
    url(r'^static/(?P<path>.*)$', st.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', st.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    # 首页
    path('', TemplateView.as_view(template_name='index.html'), name='index')
]
