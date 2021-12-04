import re

from fields.base_field import TypedField


class StringField(TypedField):
    _type = str    


class IntegerField(TypedField):
    _type = int    


class BooleanField(TypedField):
    _type = int    


class RegexField(StringField):
    regexp_pattern = None

    def __init__(self, pattern=None, **kwargs) -> None:

        if not any([self.regexp_pattern, pattern]):
            raise ValueError("Missing regex pattern")
        
        super().__init__(**kwargs)
        
        self._pattern = pattern or self.regexp_pattern
        
        try:
            re.compile(self._pattern) 
        except (TypeError, re.error):
            raise ValueError(f"{self._pattern!r} is not a valid pattern")


    def validate(self, value):
        super().validate(value)
        if not re.match(self._pattern, value, re.IGNORECASE):
            raise ValueError(f"Value {value!r} does not match regex pattern {self._pattern!r}")


class PhoneField(RegexField):
    regexp_pattern = "^(\\+359|0)8[789]\\d{7}$"