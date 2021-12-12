import logging

from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from application.authentications import BaseUserJWTAuthentication
from bookcase.models import History
from bookcase.serializers import HistorySerializer
from rest_framework.viewsets import ViewSetMixin

logger = logging.getLogger(__name__.split('.')[0])


class HistoryView(ViewSetMixin, generics.ListCreateAPIView):
    serializer_class = HistorySerializer
    authentication_classes = [BaseUserJWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user, hide=False).all().order_by('date_modified')

    @action(detail=False, methods=['post'], url_path='delete_history', serializer_class=HistorySerializer)
    def post_delete_history(self, request, *args, **kwargs):
        list_history_id = request.data.get("list_id")
        for history_id in list_history_id:
            try:
                history = History.objects.filter(id=history_id).first()
                history.hide = True
                history.save()
            except:
                Response("Error")
        return Response("Delete history success", status=status.HTTP_200_OK)
