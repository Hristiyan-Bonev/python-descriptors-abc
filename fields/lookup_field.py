from fields.base_field import Field
from fields.string_field import DictField

class OneOf(Field):

    def __init__(self, lookup_values, case_sensitive=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.lookup_values = lookup_values
        self.case_sensitive=case_sensitive

        
    def validate(self, value):
        super().validate(value)
        if value.lower() not in (x.lower() if self.case_sensitive else x for x in self.lookup_values):
            raise ValueError(f"{self._name}: Invalid value {value}")

class NestedField(DictField):

    def __init__(self, obj_initializer, *, required=False, default_value=None) -> None:
        super().__init__(required=required, default_value=default_value)
        self.obj_initializer = obj_initializer

    def validate(self, value):
        super().validate(value)
        return self.obj_initializer(**value)
