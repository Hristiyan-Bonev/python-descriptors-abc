from descriptors.base import Field
from collections import Mapping, Iterable


class TypedDescriptor(Field):
    _type = None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, self._type):
            raise TypeError(
                f"Cannot use value of type {type(value).__name__} as type {self._type}")

class StringField(TypedDescriptor):
    _type = str


class IntegerField(TypedDescriptor):
    _type = int

class BooleanField(TypedDescriptor):
    _type = int



