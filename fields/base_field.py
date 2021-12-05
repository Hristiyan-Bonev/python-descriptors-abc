from abc import ABC, abstractmethod
import os
import logging

logging.basicConfig(level=logging.DEBUG)



class Field(ABC):

    def __init__(self, *, required=False, default_value=None) -> None:
        self.required = required        
        self.default_value = default_value
        self._debug = os.environ.get('DEBUG', False)

    def __set_name__(self, owner, name):
        self._name = name
        self._combined_name = f"{owner.__name__}.{name}"

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self._name)

    def __set__(self, obj, value):
        set_value = value
        try:
            self.validate(set_value)
        except (ValueError, TypeError,) as exc:
            logging.error(f'Validation of field "{self._combined_name}" failed for value: {value!r}. Cause: {exc} ')
            if self.required:
                raise exc
        
            if self.default_value != None:
                logging.warning(f'Using default value as fallback. Value: {self.default_value}')
                set_value = self.default_value
        
        
        logging.debug(f'Setting "{obj.__class__.__name__}.{self._name}" to {set_value!r}')
        obj.__dict__[self._name] = set_value

    @abstractmethod
    def validate(self, value):
        pass


class TypedField(Field):
    _type = None
    def validate(self, value):
        if not isinstance(value, self._type):
            raise TypeError(
                f"Cannot use value of type {type(value).__name__} as type {self._type}")
        return value