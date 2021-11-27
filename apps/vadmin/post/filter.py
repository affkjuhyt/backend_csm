import django_filters

from apps.vadmin.post.models import PostGroup


class PostGroupDataFilter(django_filters.rest_framework.FilterSet):
    """
    Phan loai du lieu
    """

    content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        models = PostGroup
        fields = '__all__'
