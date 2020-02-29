"""Utility types and functions."""
from typing import Any, Callable, Optional, Sequence, TypeVar

T = TypeVar('T')
Validator = Callable[[Optional[str], Any, T], bool]


class CheckedProperty:
    """Helper to have a validated member in a dataclass.

    Dataclasses don't really play very well with properties, so this works
    around that issue.

    Args:
        validators: Predicates to run agains a value when set.
        default: Default value for the property.
    """

    def __init__(
        self, validators: Sequence[Validator[T]] = (), default: Optional[T] = None
    ):
        self.validators = validators
        self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __set__(self, instance, value: T):
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


class Wrapper:
    """Helper to wrap a member's attributes.

    Args:
        wrapped_getter:
    """

    def __init__(self, wrapped_getter):
        self.wrapped_getter = wrapped_getter
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return getattr(self.wrapped_getter(instance), self.name)

    def __delete__(self, instance):
        delattr(self.wrapped_getter(instance), self.name)

    def __set__(self, instance, value):
        if value is self:
            return

        setattr(self.wrapped_getter(instance), self.name, value)


def wrapper(*args, **kwargs) -> Any:
    """Type-erased constructor for CheckedProperty."""
    return Wrapper(*args, **kwargs)
