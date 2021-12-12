from rest_framework_extensions.routers import ExtendedSimpleRouter

from userprofile.apis.v1 import UserPublicView, UpdateInfo,\
    FollowBookAdminView, DownloadBookAdminView, UserFollowingViewSet, UserGroupViewSet

public_router = ExtendedSimpleRouter()

public_router.register(
    r'user-profile',
    UserPublicView,
    basename='v1-user-profile'
)

# public_router.register(
#     r'update-account',
#     UpdateInfo,
#     basename='v1-update-account'
# )

userprofile_urlpatterns = public_router.urls


private_router = ExtendedSimpleRouter()

private_router.register(
    r'follow',
    FollowBookAdminView,
    basename='v1-follow'
)

private_router.register(
    r'download',
    DownloadBookAdminView,
    basename='v1-list-download'
)

private_router.register(
    r'follow-user',
    UserFollowingViewSet,
    basename='v1-follow-user'
)

private_router.register(
    r'groups',
    UserGroupViewSet,
    basename='v1-groups'
)

follow_urlpatterns = private_router.urls
