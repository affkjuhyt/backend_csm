from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.permission.views import MenuModelViewSet, DeptModelViewSet, RoleModelViewSet, \
    UserProfileModelViewSet

router = DefaultRouter()
router.register(r'menus', MenuModelViewSet)
router.register(r'dept', DeptModelViewSet)
router.register(r'dept/exclude', DeptModelViewSet)
router.register(r'role', RoleModelViewSet)
router.register(r'user', UserProfileModelViewSet)
urlpatterns = [

    re_path('dept/exclude/(?P<pk>.*)/', DeptModelViewSet.as_view({'get': 'exclude_list'})),
    re_path('dept/treeselect/', DeptModelViewSet.as_view({'get': 'tree_select_list'})),
    re_path('menus/treeselect/', MenuModelViewSet.as_view({'get': 'tree_select_list'})),
    re_path('menus/roleMenuTreeselect/(?P<pk>.*)/', MenuModelViewSet.as_view({'get': 'role_menu_tree_select'})),
    re_path('dept/roleDeptTreeselect/(?P<pk>.*)/', DeptModelViewSet.as_view({'get': 'role_dept_tree_select'})),
    re_path('user/changeStatus/', UserProfileModelViewSet.as_view({'put': 'change_status'})),
    re_path('user/details/', UserProfileModelViewSet.as_view({'get': 'get_user_details'})),
    re_path('user/resetPwd/', UserProfileModelViewSet.as_view({'put': 'reset_pwd'})),
    re_path('user/profile/updatePwd/', UserProfileModelViewSet.as_view({'put': 'update_pwd'})),
    re_path('user/profile/avatar/', UserProfileModelViewSet.as_view({'put': 'put_avatar'})),
    re_path('user/profile/', UserProfileModelViewSet.as_view({'get': 'profile', 'put': 'put_profile'})),
    re_path('user/export/', UserProfileModelViewSet.as_view({'get': 'export', })),
    re_path('role/export/', RoleModelViewSet.as_view({'get': 'export', })),
    re_path('user/importTemplate/',
            UserProfileModelViewSet.as_view({'get': 'importTemplate', 'post': 'importTemplate'})),

]
urlpatterns += router.urls
