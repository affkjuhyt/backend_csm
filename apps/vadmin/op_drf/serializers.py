from django.utils.functional import cached_property

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import BindingDict


class CustomModelSerializer(ModelSerializer):

    modifier_field_name = 'modifier'
    creator_field_name = 'creator'
    dept_belong_id_field_name = 'dept_belong_id'
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator_name = serializers.SlugRelatedField(slug_field="username", source="creator", read_only=True)

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        if self.context.get('request'):
            self.request = self.context.get('request')
        if self.request:
            username = self.get_request_username()
            if self.modifier_field_name in self.fields.fields:
                validated_data[self.modifier_field_name] = username
            if self.creator_field_name in self.fields.fields:
                validated_data[self.creator_field_name] = self.request.user
            if self.dept_belong_id_field_name in self.fields.fields:
                validated_data[self.dept_belong_id_field_name] = getattr(self.request.user, 'dept_id', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.request:
            if hasattr(self.instance, self.modifier_field_name):
                self.instance.modifier = self.get_request_username()
        return super().update(instance, validated_data)

    def get_request_username(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'username', None)
        return None

    @cached_property
    def fields(self):
        fields = BindingDict(self)
        for key, value in self.get_fields().items():
            fields[key] = value

        if not hasattr(self, '_context'):
            return fields
        is_root = self.root == self
        parent_is_list_root = self.parent == self.root and getattr(self.parent, 'many', False)
        if not (is_root or parent_is_list_root):
            return fields

        try:
            request = self.request or self.context['request']
        except KeyError:
            return fields
        params = getattr(
            request, 'query_params', getattr(request, 'GET', None)
        )
        if params is None:
            pass
        try:
            filter_fields = params.get('_fields', None).split(',')
        except AttributeError:
            filter_fields = None

        try:
            omit_fields = params.get('_omit', None).split(',')
        except AttributeError:
            omit_fields = []

        existing = set(fields.keys())
        if filter_fields is None:
            allowed = existing
        else:
            allowed = set(filter(None, filter_fields))

        omitted = set(filter(None, omit_fields))
        for field in existing:
            if field not in allowed:
                fields.pop(field, None)
            if field in omitted:
                fields.pop(field, None)

        return fields



