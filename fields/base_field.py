from abc import ABC, abstractmethod
import os
import logging

DEBUG = os.environ.get('DEBUG', False)

class Field(ABC):

    def __init__(self, *, strict=False, default_value=None) -> None:
        self.strict = strict
        self.default_value = default_value

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self._name)

    def __set__(self, obj, value):
        set_value = self._validate(value)
        if DEBUG:
            logging.debug(f'Setting "{obj.__class__.__name__}.{self._name}" to {set_value!r}')

        obj.__dict__[self._name] = set_value

    @abstractmethod
    def validate(self, value):
        pass

    def _validate(self, value):
        try:
            self.validate(value)
            return value
        except ValueError as e:
            logging.info(f'Validation failed for {value!r}. Cause: {e} ')
            if self.strict:
                raise e

            if self.default_value:
                if DEBUG:
                    logging.warning(f'Using fallback default value: {value}')
                return self.default_value

        except Exception as exc:
            logging.exception(f"Got unexpected exception while setting {value}.")

class TypedField(Field):

    _type = None

    def validate(self, value):
        if not isinstance(value, self._type):
            raise ValueError(
                f"Cannot use {type(value)} as it's not of type {type(self._type)}")


class StringField(TypedField):
    _type = str    
