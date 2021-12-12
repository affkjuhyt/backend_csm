import logging

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from books.models import Tag
from books.serializers import TagSerializer

logger = logging.getLogger(__name__.split('.')[0])


class TagView(ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return Tag.objects.filter().order_by('?')

