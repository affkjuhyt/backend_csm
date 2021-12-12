from rest_framework_extensions.routers import ExtendedSimpleRouter

from bookcase.apis.v1 import HistoryView

private_router = ExtendedSimpleRouter()

private_router.register(
    r'history',
    HistoryView,
    basename='v1-history'
)

history_urlpatterns = private_router.urls
