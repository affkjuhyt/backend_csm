import json
import logging
import operator
from functools import reduce

from django.utils import six
from mongoengine.queryset import visitor
from rest_framework.filters import BaseFilterBackend, SearchFilter, OrderingFilter

from apps.vadmin.utils.model_util import get_dept

logger = logging.getLogger(__name__)


def get_as_kwargs(request):
    params = request.GET.dict()
    if 'as' not in params:
        return {}
    as_params = json.loads(params.get('as', '{}'))
    return as_params


class MongoSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        search_terms = self.get_search_terms(request)
        if not search_fields or not search_terms:
            return queryset
        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]
        if not orm_lookups:
            return queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                visitor.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))
        return queryset


class MongoOrderingFilter(OrderingFilter):

    def get_valid_fields(self, queryset, view, context={}):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if valid_fields is None:
            return self.get_default_valid_fields(queryset, view, context)
        elif valid_fields == '__all__':
            # View explicitly allows filtering on any models field
            model = view.get_serializer().__class__.Meta.model
            valid_fields = [
                (field_name, getattr(field, 'verbose_name', field_name)) for field_name, field in model._fields.items()
            ]
        else:
            valid_fields = [
                (item, item) if isinstance(item, six.string_types) else item
                for item in valid_fields
            ]

        return valid_fields


class AdvancedSearchFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        as_kwargs = get_as_kwargs(request)
        if as_kwargs:
            queryset = queryset.filter(**as_kwargs)
        return queryset


class MongoAdvancedSearchFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        as_kwargs = get_as_kwargs(request)
        if as_kwargs:
            queryset = queryset.filter(**as_kwargs)
        return queryset


class DataLevelPermissionsFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        # user_dept_id = getattr(request.user, 'dept_id')
        # if not user_dept_id:
        #     return queryset.none()

        if not getattr(queryset.model, 'dept_belong_id', None):
            return queryset

        # if not hasattr(request.user, 'role'):
        #     return queryset.filter(dept_belong_id=user_dept_id)

        role_list = request.user.role.filter(status='1').values('admin', 'dataScope')
        dataScope_list = []
        for ele in role_list:
            if '1' == ele.get('dataScope') or ele.get('admin') == True:
                return queryset
            dataScope_list.append(ele.get('dataScope'))
        dataScope_list = list(set(dataScope_list))

        if dataScope_list == ['5']:
            return queryset.filter(creator=request.user)

        dept_list = []
        for ele in dataScope_list:
            if ele == '2':
                dept_list.extend(request.user.role.filter(status='1').values_list('dept__id', flat=True))
            elif ele == '3':
                dept_list.extend(request.user.role.filter(status='1').values_list('dept__id', flat=True))
            elif ele == '4':
                dept_list.extend(request.user.role.filter(status='1').values_list('dept__id', flat=True))
        return queryset.filter(dept_belong_id__in=list(set(dept_list)))
