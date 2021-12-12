import logging

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

from application.authentications import BaseUserJWTAuthentication
from books.models import Image
from books.serializers import ImageSerializer

logger = logging.getLogger(__name__.split('.')[0])


class ImageView(ViewSetMixin, generics.RetrieveUpdateAPIView, generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    authentication_classes = [BaseUserJWTAuthentication]

    def get_queryset(self):
        return Image.objects.filter()

    @action(detail=False, methods=['post'], url_path='add_image', serializer_class=ImageSerializer)
    def post_image(self, request):
        data = request.data
        chapter = data.get('chapter')
        post = data.get('post')
        image = request.FILES['image']

        try:
            response = {}
            image = Image.objects.create(chapter_id=chapter, post_id=post, image=image)
            image.save()
            response['id'] = image.id
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response("Create image failed", status=status.HTTP_404_NOT_FOUND)
