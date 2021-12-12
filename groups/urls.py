from rest_framework_extensions.routers import ExtendedSimpleRouter

from groups.apis.v1 import GroupView

public_router = ExtendedSimpleRouter()

public_router.register(
    r'groups',
    GroupView,
    basename='v1-groups'
)

group_public_urlpatterns = public_router.urls
