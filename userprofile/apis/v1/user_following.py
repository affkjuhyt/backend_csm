from rest_framework import viewsets, generics
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.viewsets import ViewSetMixin

from application.authentications import BaseUserJWTAuthentication
from userprofile.models import UserFollowing
from userprofile.serializers import UserFollowingSerializer


class UserFollowingViewSet(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = UserFollowingSerializer
    authentication_classes = [BaseUserJWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        return UserFollowing.objects.filter(user_id=user)


