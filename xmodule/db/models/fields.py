from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property


class ChoiceEnum(Enum):
    def __str__(self):
        return self.verbose_name

    def __json__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            other = other.value

        return other == self.value

    def __ne__(self, other):
        if isinstance(other, type(self)):
            other = other.value

        return other != self.value

    def __hash__(self):
        return hash(self.value)

    def __int__(self):
        return self.value

    @cached_property
    def verbose_name(self):
        return self.name.replace('_', ' ').title()

    @classmethod
    def choices(cls):
        choices = []
        members = cls.__members__
        for k in sorted(members.keys()):
            enum_value = members[k]
            choices.append((enum_value.value, enum_value.verbose_name))

        return choices

    @classmethod
    def reverse(cls, value):
        for v in cls.__members__.values():
            if v.value == value:
                return v

        raise KeyError(value)


class ChoiceEnumField(models.CharField):
    default_error_messages = {
        'invalid': '“%(value)s” value must be a valid choice.',
    }

    def __init__(self, enum, **kwargs):
        assert issubclass(enum, ChoiceEnum), '`enum` must be subclass of ChoiceEnum'
        self.enum = enum
        self.default_enum = kwargs.get('default')

        if self.default_enum is not None:
            if isinstance(self.default_enum, str):
                self.default_enum = self.enum.reverse(self.default_enum)

            self._assert_type(self.default_enum)
            kwargs['default'] = self.default_enum.value

        kwargs['choices'] = enum.choices()
        kwargs['max_length'] = max(len(k) for k, v in kwargs['choices'])
        super().__init__(**kwargs)

    def _assert_type(self, value):
        assert isinstance(value, self.enum), 'Expecting instance of %s. Got %s' % (
            self.enum.__name__, type(value).__name__
        )

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, self.enum):
            return value.value

        return value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, self.enum):
            return value

        value = super().to_python(value)
        if value is None:
            return value

        try:
            return self.enum(value)
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def deconstruct(self):
        name, path, _, kwargs = super().deconstruct()
        if self.default_enum:
            kwargs['default'] = self.default_enum

        kwargs.pop('choices', None)
        return name, path, [self.enum], kwargs

    def validate(self, value, model_instance):
        if isinstance(value, self.enum):
            value = value.value

        return super().validate(value, model_instance)

    def run_validators(self, value):
        if isinstance(value, self.enum):
            value = value.value

        return super().run_validators(value)
