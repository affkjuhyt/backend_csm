import django_filters

from apps.vadmin.group.models import Group, GroupUser


class GroupDataFilter(django_filters.rest_framework.FilterSet):
    """
    Phan loai du lieu
    """

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        models = Group
        fields = '__all__'
