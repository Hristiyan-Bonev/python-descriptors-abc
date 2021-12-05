from descriptors.base import Field
from collections import Mapping, Iterable

class TypedDescriptor(Field):
    _type = None

    def validate(self, value):
        if not isinstance(value, self._type):
            import ipdb; ipdb.set_trace()
            raise TypeError(
                f"Cannot use value of type {type(value).__name__} as type {self._type}")
        # return value

class StringField(TypedDescriptor):
    _type = str    


class IntegerField(TypedDescriptor):
    _type = int    


class BooleanField(TypedDescriptor):
    _type = int    


class DictField(TypedDescriptor):
    _type = Mapping

class IterableField(TypedDescriptor):
    _type = Iterable