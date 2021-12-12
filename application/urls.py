"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from captcha.conf import settings as ca_settings
from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import re_path, include, path
from django.views.static import serve
from rest_framework.views import APIView

from apps.vadmin.op_drf.response import SuccessResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

from authen import views
from authen.urls import auth_urlpatterns
from bookcase.urls import history_urlpatterns
from books.urls import books_public_urlpatterns, books_urlpatterns
from groups.urls import group_public_urlpatterns
from posts.urls import post_public_urlpatterns, post_urlpatterns
from userprofile.urls import follow_urlpatterns, userprofile_urlpatterns

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


external_public_urlpatterns = books_public_urlpatterns + post_public_urlpatterns \
                              + group_public_urlpatterns
external_urlpatterns = follow_urlpatterns + auth_urlpatterns + history_urlpatterns + books_urlpatterns \
                       + post_urlpatterns + userprofile_urlpatterns


urlpatterns = [
    path('admin1/', admin.site.urls),
    path('v1/public/', include(external_public_urlpatterns)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/', include(external_urlpatterns)),
    path('signingg', views.GoogleView.as_view(), name='sigin-gg'),
    path('signinfb', views.FacebookView.as_view(), name='sigin-fb'),
    path('signinapple', views.AppleView.as_view(), name='sigin-apple'),
    path('login', views.LoginAPI.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view()),
    # re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'^admin/', include('apps.vadmin.urls')),
    url(r'^collect/', include('collector.urls')),
    url(r'^rec/', include('recommender.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
