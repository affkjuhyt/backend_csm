from django.urls import re_path
from rest_framework.routers import DefaultRouter

from posts.views import PostGroupDataModelViewSet
from apps.vadmin.system.views import DictDataModelViewSet, DictDetailsModelViewSet, \
    ConfigSettingsModelViewSet, SaveFileModelViewSet, MessagePushModelViewSet, LoginInforModelViewSet, \
    OperationLogModelViewSet, CeleryLogModelViewSet, SystemInfoApiView, DashboardApiView, BookBarChartView, \
    PieChartApiView, \
    BarChartApiView, GetCommentDayView, PercentUserApiView, RegisterUserApiView

from books.views import BookDataModelViewSet, ChapterDataModelViewSet, ChapterAdminViewSet, \
    ImageDataModelViewSet, CommentAdminViewSet, BookDataAdminViewSet, VulgarAdminViewSet

from groups.views import GroupDataModelViewSet

router = DefaultRouter()
router.register(r'dict/type', DictDataModelViewSet)
router.register(r'dict/data', DictDetailsModelViewSet)
router.register(r'book/data', BookDataModelViewSet)
router.register(r'book/chapter', ChapterDataModelViewSet)
router.register(r'group', GroupDataModelViewSet)
router.register(r'post', PostGroupDataModelViewSet)
router.register(r'comment', CommentAdminViewSet, basename='comment')
router.register(r'vulgar', VulgarAdminViewSet, basename='vulgar')
router.register(r'config', ConfigSettingsModelViewSet)
router.register(r'savefile', SaveFileModelViewSet)
router.register(r'image', ImageDataModelViewSet)
router.register(r'message', MessagePushModelViewSet)
router.register(r'logininfor', LoginInforModelViewSet)
router.register(r'operation_log', OperationLogModelViewSet)
router.register(r'celery_log', CeleryLogModelViewSet)

urlpatterns = [
    re_path('dict/get/type/(?P<pk>.*)/', DictDetailsModelViewSet.as_view({'get': 'dict_details_list'})),
    re_path('config/configKey/(?P<pk>.*)/', ConfigSettingsModelViewSet.as_view({'get': 'get_config_key'})),
    re_path('config/export/', ConfigSettingsModelViewSet.as_view({'get': 'export'})),
    re_path('config/clearCache/', ConfigSettingsModelViewSet.as_view({'delete': 'clearCache', })),
    re_path('dict/type/export/', DictDataModelViewSet.as_view({'get': 'export'})),
    re_path('dict/data/export/', DictDetailsModelViewSet.as_view({'get': 'export'})),
    # export data book
    re_path('book/data/export/', BookDataModelViewSet.as_view({'get': 'export'})),
    re_path('book/data/update', BookDataAdminViewSet.as_view({'put': 'update_book'})),
    # export data chapter
    re_path('book/chapter/export/', ChapterDataModelViewSet.as_view({'get': 'export'})),
    re_path('book/chapter/update/', ChapterAdminViewSet.as_view({'put': 'update_chapter'})),
    re_path('dict/type/clearCache/', DictDetailsModelViewSet.as_view({'delete': 'clearCache', })),
    # export data vulgar
    re_path('vulgar/export', VulgarAdminViewSet.as_view({'get': 'export'})),
    # export Group
    re_path('group/export', GroupDataModelViewSet.as_view({'get': 'export'})),
    # clearCache group
    re_path('group/clearCache', GroupDataModelViewSet.as_view({'delete': 'clearCache'})),
    re_path('message/export/', MessagePushModelViewSet.as_view({'get': 'export', })),
    re_path('message/user_messages/', MessagePushModelViewSet.as_view({'get': 'get_user_messages', })),
    re_path('message/is_read/(?P<pk>.*)/', MessagePushModelViewSet.as_view({'put': 'update_is_read', })),
    re_path('operation_log/clean/', OperationLogModelViewSet.as_view({'delete': 'clean_all', })),
    re_path('operation_log/export/', OperationLogModelViewSet.as_view({'get': 'export', })),
    re_path('logininfor/clean/', LoginInforModelViewSet.as_view({'delete': 'clean_all', })),
    re_path('logininfor/export/', LoginInforModelViewSet.as_view({'get': 'export', })),
    re_path('celery_log/clean/', CeleryLogModelViewSet.as_view({'delete': 'clean_all', })),
    re_path('celery_log/export/', CeleryLogModelViewSet.as_view({'get': 'export', })),
    re_path('clearsavefile/', SaveFileModelViewSet.as_view({'post': 'clearsavefile', })),
    re_path('clearimagefile/', ImageDataModelViewSet.as_view({'post': 'clearimagefile', })),
    re_path('sys/info/', SystemInfoApiView.as_view()),
    re_path('dashboard/', DashboardApiView.as_view()),
    re_path('percentUser/', PercentUserApiView.as_view()),
    re_path('registerUser/', RegisterUserApiView.as_view()),
    re_path('book/barchart', BookBarChartView.as_view()),
    re_path('piechart/', PieChartApiView.as_view()),
    re_path('barchart/', BarChartApiView.as_view()),
    re_path('comment/weekday/', GetCommentDayView.as_view())
]
urlpatterns += router.urls
