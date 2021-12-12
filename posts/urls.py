from rest_framework_extensions.routers import ExtendedSimpleRouter

from posts.apis.v1 import PostView, PostAdminView

public_router = ExtendedSimpleRouter()

public_router.register(
    r'posts',
    PostView,
    basename='v1-posts'
)

post_public_urlpatterns = public_router.urls

private_router = ExtendedSimpleRouter()

private_router.register(
    r'posts',
    PostAdminView,
    basename='v1-posts'
)

post_urlpatterns = private_router.urls
