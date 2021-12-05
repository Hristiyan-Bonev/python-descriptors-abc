from typing import Callable
from descriptors.base import Field
from collections import Mapping, Iterable


class ValidatorFunction:
    def __init__(self, fn: Callable, err_msg: str) -> None:
        self.fn = fn
        self.err_msg = err_msg
        self.name = fn.__qualname__

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

positive_integer = ValidatorFunction(lambda x: x>0, "Number must be > 0")
even_integer = ValidatorFunction(lambda x: x>0, "Number must even")

class TypedDescriptor(Field):
    _type = None
    _additional_validators = []

    def __init__(self, additional_validators=None, *, required=False, default_value=None) -> None:
        super().__init__(required=required, default_value=default_value)
        self._additional_validators = additional_validators or self._additional_validators

        for validator in self._additional_validators:
            if not isinstance(validator, ValidatorFunction):
                raise TypeError(f"Validator {validator} is not of type ValidatorFunction")

    def validate(self, value):
        if not isinstance(value, self._type):
            raise TypeError(
                f"Cannot use value of type {type(value).__name__} as type {self._type}")
        for validator in self._additional_validators:
            _errors = []
            if not validator(value):
                raise ValueError(f"validator {validator.name} failed for value {value}. Error message: {validator.err_msg}")
            for err in _errors:
                raise err

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
