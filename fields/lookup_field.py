from fields.base_field import Field
from fields.string_field import DictField, StringField, IterableField

class OneOf(StringField):

    def __init__(self, lookup_values, case_sensitive=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.case_sensitive=case_sensitive
        self.lookup_values = [name if case_sensitive else name.lower() for name in lookup_values]

        
    def validate(self, value):
        super().validate(value)
        if value.lower() not in self.lookup_values:
            raise ValueError(f"{self._name}: Invalid value {value}")

class NestedField(DictField):

    def __init__(self, obj_initializer, *, required=False, default_value=None) -> None:
        super().__init__(required=required, default_value=default_value)
        self.obj_initializer = obj_initializer

    def validate(self, obj, value):

        init_values = value or self.default_value or {}

        # Create instance with the provided values

        obj = self.obj_initializer(**init_values).__dict__
        import ipdb;ipdb.set_trace()

        super().validate(obj, obj.__dict__)


        # # Provide created instance dictionary to be set through parent set method
        # return super().__set__(obj, inst.__dict__)

class ObjectContainer(NestedField):
    def __set__(self, obj, value):
        import ipdb;ipdb.set_trace()
        super(IterableField, self).validate(value)
        ee = []
        for val in value:
            ee.append(super().validate(obj, val))
        super().__set__(obj, value)

    def vali