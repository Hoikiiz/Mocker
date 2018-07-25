from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

__author__ = 'sun_yang'

router = DefaultRouter()
router.register(r'mockItem', views.MockItemViewSet)
router.register(r'mockSlot', views.MockSlotViewSet)
router.register(r'mockCondition', views.MockConditionViewSet)

schema_view = get_swagger_view(title='Mocker API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/$', schema_view),
    url(r'^queryLogs', views.query_logs, name='query_logs'),
    url(r'^(.*)', views.mocker, name='mocker'),
]

item_list = views.MockItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
item_detail = views.MockItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
slot_list = views.MockSlotViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
slot_detail = views.MockSlotViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
condition_list = views.MockConditionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
condition_detail = views.MockConditionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
