from descriptors.base import Field


class OneOf(Field):

    def __init__(self, lookup_values, case_sensitive=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.case_sensitive = case_sensitive
        self.lookup_values = [name if case_sensitive else name.lower()
                              for name in lookup_values]

    def validate(self, value):
        if value not in self.lookup_values:
            raise ValueError(
                f"Value {value} is not one of {self.lookup_values}")


class ModelField(Field):

    def __init__(self, obj_initializer, **kwargs) -> None:
        super().__init__(**kwargs)
        self.obj_initializer = obj_initializer
        self.temp_obj = None

    def validate(self, values):
        self.temp_obj = self.obj_initializer(**values)

    def _set_value(self, obj, value):
        obj.__dict__[self._name] = self.temp_obj
        self.temp_obj = None
