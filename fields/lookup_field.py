from fields.base_field import Field, StringField

class DictLookupField(Field):

    def __init__(self, lookup_dict, *, strict=False, default_value=None) -> None:
        super().__init__(strict=strict, default_value=default_value)
        self.lookup_dict = lookup_dict
        
    def validate(self, value):
        super().validate(value)
        
        if value.lower() not in self.lookup_dict:
            raise ValueError(f"{self._name}: Invalid value {value}")