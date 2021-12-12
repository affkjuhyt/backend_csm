from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework import serializers
# from django.core import serializers
from drf_yasg import openapi
from rest_framework import mixins, viewsets



def custom_view(detail=True, method='posts'):
    class CustomClass(
        APIView
    ):
        model = None

        def get_queryset(self):
            return self.model.nodes.all()

        def get_object(self, pk):
            try:
                return self.model.nodes.get(uuid=pk)
            except:
                raise Http404

    def inner_func(self, request):
        pass

    def inner_detail_funcc(self, request, pk):
        pass

    if detail:
        func = inner_detail_funcc
    else:
        func = inner_func

    setattr(CustomClass, method, func)

    return CustomClass


class BaseDetailPostView(
    APIView
):
    model = None

    def get_queryset(self):
        return self.model.nodes.all()

    def get_object(self, pk):
        try:
            return self.model.nodes.get(uuid=pk)
        except:
            raise Http404

    def post(self, request, pk):
        obj = self.get_object(pk)
        obj.update_attributes(request.data)
        obj.save()
        obj.refresh()
        return Response(obj.serialize, status=status.HTTP_200_OK)


class BaseDetailView(
    APIView
):
    model = None

    def get_queryset(self):
        return self.model.nodes.all()

    def get_object(self, pk):
        try:
            return self.model.nodes.get(uuid=pk)
        except:
            raise Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        return Response(queryset.serialize, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        obj.update_attributes(request.data)
        obj.save()
        obj.refresh()
        return Response(obj.serialize, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response({}, status=status.HTTP_200_OK)


class BaseListView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    model = None

    def get_queryset(self):
        return self.model.nodes.all()

    def get(self, request):
        queryset = self.get_queryset()
        return Response(
            # self.serializer_class(queryset, context={'request': request}, many=True).data,
            [self.serializer_class(n, context={'request': request}, many=True).data for n in queryset],
            status=status.HTTP_200_OK
        )

    def post(self, request):
        obj = self.model()
        obj.update_attributes(request.data)
        obj.save()
        return Response(obj.serialize, status=status.HTTP_200_OK)


class BaseSerializer(serializers.Serializer):
    """
    Serializing Base
    """
    properties = {}
    required = []

    class Meta:
        swagger_schema_fields = {}

    def __init__(self, *args, **kwargs) :
        self.Meta.swagger_schema_fields = {
            "properties": {
                "uuid": openapi.Schema(
                    title="uuid",
                    type=openapi.TYPE_STRING,
                ),
                **self.properties
            },
        }
        super(BaseSerializer, self).__init__(*args, **kwargs)
