import logging

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from books.models import HistorySearch
from books.serializers import HistorySearchSerializer
from application.authentications import BaseUserJWTAuthentication

logger = logging.getLogger(__name__.split('.')[0])


class HistorySearchView(ReadOnlyModelViewSet):
    serializer_class = HistorySearchSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    authentication_classes = [BaseUserJWTAuthentication]

    def get_queryset(self):
        return HistorySearch.objects.filter(user=self.request.user).order_by('-date_added')[:5]

    @action(detail=False, methods=['get'], url_path='trend', serializer_class=HistorySearchSerializer)
    def get_relate_to(self, request, *args, **kwargs):
        histories = HistorySearch.objects.filter(user=self.request.user).order_by('-date_added')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(histories, request)
        serializer = HistorySearchSerializer(result_page, context={"request": request}, many=True)
        return paginator.get_paginated_response(serializer.data)
