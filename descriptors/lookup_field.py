from logging import exception
from typing import Type
from descriptors.base import Field
from descriptors.typed import DictField, StringField, IterableField

class OneOf(Field):

    def __init__(self, lookup_values, case_sensitive=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.case_sensitive=case_sensitive
        self.lookup_values = [name if case_sensitive else name.lower() for name in lookup_values]

        
    def validate(self, value):
        super().validate(value)
        if value.lower() not in self.lookup_values:
            raise ValueError(f"{self._name}: Invalid value {value}")

class ModelField(Field):

    def __init__(self, obj_initializer, **kwargs) -> None:
        super().__init__(**kwargs)
        self.obj_initializer = obj_initializer

    def validate(self, values):
        self.obj_initializer(**values)   