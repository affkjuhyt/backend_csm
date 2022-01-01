from rest_framework.validators import UniqueValidator, qs_exists

from apps.vadmin.utils.exceptions import APIException


class CustomUniqueValidator(UniqueValidator):

    def __call__(self, value, serializer_field):
        # Determine the underlying models field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        field_name = serializer_field.source_attrs[-1]
        # Determine the existing instance, if this is an update operation.
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if qs_exists(queryset):
            raise APIException(message=self.message)

    def __repr__(self):
        return super().__repr__()
