from abc import ABC, abstractmethod
import os
import logging

logging.basicConfig(level=logging.ERROR)


class Field(ABC):

    _external_validators = []

    def __init__(self, *, required=False, default_value=None, external_validators=None) -> None:
        self.required = required
        self.default_value = default_value

        if not external_validators:
            external_validators = []
        self.validators = []
        self.validators = self._external_validators + external_validators
        print(self._external_validators)

        assert(callable(x)
               for x in self._external_validators), "Only callables should be passed as validators"

    def __set_name__(self, owner, name):
        self._name = name
        self._combined_name = f"{owner.__name__}.{name}".lower()

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self._name)

    def __set__(self, obj, value):
        """
        Iterate through class validation method as well as the external validators (if any), making sure
        that the value is valid against every one of them. 
        """

        for x in [self.validate, *self.validators]:
            self.apply_validation(x, obj, value)

        self._set_value(obj, value)

    def apply_validation(self, function, obj, value):
        """
        Apply validation function against the given value.
        If an exception is raised, this function check if the `obj` contains `errors_list` attribute 
        and stores metadata about the failed validation 
        """
        try:
            function(value)
        except (ValueError, TypeError,) as exc:
            logging.error(
                f'Function "{function.__name__}" failed for field "{self._combined_name}" and value: {value!r}. Cause: {exc} ')

            if self.default_value != None:
                logging.warning(
                    f'Using default value as fallback. Value: {self.default_value}')
                value = self.default_value

            if getattr(obj, 'errors_list') != None:
                obj.errors_list.append(
                    {
                        "field_name": self._combined_name,
                        "validator_name": function.__qualname__,
                        "error_type": type(exc).__name__,
                        "error_message": " ".join(exc.args),
                        "value": value
                    })

    def _set_value(self, obj, value):
        logging.debug(f'Setting "{self._combined_name}" to {value!r}')
        obj.__dict__[self._name] = value

    @abstractmethod
    def validate(self, value) -> None:
        """
        A method that contains implementation details about how each subclass will perform.
        Used as abstract method, because we want to make sure each subclass is implementing it.

        This method expects to return either `None` or to raise an exception to indicate that a given
        value is not valid.

        Expected exceptions: ValueError, TypeError
        """
        pass
