from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from authen.apis.v1 import RegisterViewSet, PasswordViewSet

router = SimpleRouter()
router.register(
    r'register',
    RegisterViewSet,
    basename='register'
)

router.register(
    r'passwords',
    PasswordViewSet,
    basename='passwords'
)

auth_urlpatterns = [
    url(r'^auth/', include(router.urls)),
]
