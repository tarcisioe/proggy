"""Utility types and functions."""
from typing import Any


class CheckedProperty:
    """Helper to have a validated member in a dataclass.

    Dataclasses don't really play very well with properties, so this works
    around that issue.

    Args:
        validators: functions
    """
    def __init__(self, validators=(), default=None):
        self.validators = validators
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value is self:
            if self.default is not None:
                value = self.default
            else:
                type_name = type(instance).__name__
                raise ValueError(
                    f'Attribute "{self.name}" on type {type_name} has '
                    'no default value and none was provided.'
                )

        for validator in self.validators:
            validator(self.name, instance, value)
        instance.__dict__[self.name] = value


def checked_property(*args, **kwargs) -> Any:
    """Type-erased constructor for CheckedProperty."""
    return CheckedProperty(*args, **kwargs)
