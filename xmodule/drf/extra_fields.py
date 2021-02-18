from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_text
from rest_framework import serializers

from xmodule.utils.strings import underscore_to_camel, camel_to_underscore


class ChoiceEnumSerializerField(serializers.IntegerField):
    default_error_messages = {
        'invalid': 'A valid enum value is required.'
    }

    def __init__(self, enum, output_attr='value', **kwargs):
        self.enum = enum
        self.output_attr = output_attr
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        try:
            return self.enum(value)
        except ValueError:
            self.fail('invalid')

    def to_representation(self, value):
        if isinstance(value, self.enum):
            return getattr(value, self.output_attr)

        return super().to_representation(value)


class SlugOrPrimaryKeyField(serializers.SlugRelatedField):
    pk_field = 'pk'

    def __init__(self, pk_field=None, **kwargs):
        self.pk_field = pk_field or self.pk_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.pk_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.pk_field, value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def get_default(self):
        default = super().get_default()
        qs = self.get_queryset()
        if isinstance(default, qs.model):
            return default

        return qs.get(**{self.pk_field: default})


class CaseInterOpField(serializers.CharField):
    def to_representation(self, value):
        return underscore_to_camel(value) if value else value

    def to_internal_value(self, data):
        return camel_to_underscore(data) if data else data
