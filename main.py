from traitlets.traitlets import default
from resources.auto_manufacturers import MANUFACTURERS
from fields.lookup_field import NestedField, OneOf, DictField
from fields.string_field import PhoneField, StringField
from fields.base_field import Field

import inspect

def _custom_init(self, *args, **kwargs):

    sig = self.__signature__.bind(*args,**kwargs)
    sig.apply_defaults()
    for attr_name, attr in sig.arguments.items(): 
        setattr(self, attr_name, attr)
    

class InitMeta(type):
    def __new__(cls, bases, dicts, class_attrs):
        class_obj = super().__new__(cls, bases, dicts, class_attrs)

        init_params = []
        for attr_name, attr in class_obj.__dict__.items():
            if isinstance(attr, Field):
                param = inspect.Parameter(attr_name, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=attr.__dict__.get(
                    'default_value', inspect.Parameter.empty))
                init_params.append(param)

        setattr(class_obj, '__signature__', inspect.Signature(parameters=init_params))
        setattr(class_obj, '__init__', _custom_init)
        
        return class_obj

class Bar(metaclass=InitMeta):
    barprop = StringField(default_value="NOT SET")


class Foo(metaclass=InitMeta):
    username = StringField()
    address = StringField(default_value="F")
    barprop = NestedField(Bar)

class CarAd(metaclass=InitMeta):
    car_manufacturer = OneOf(lookup_values=MANUFACTURERS)
    contact_phone = PhoneField(required=True)
    car_fuel_type = OneOf(["Дизел", "Бензин", "Газ/Бензин",
                          "Метан/Бензин", "Хибрид"], case_sensitive=True)
    related = NestedField(Foo) 

    def __init__(self, *args, **kwargs) -> None:
        [setattr(self, name, val) for name, val in self.__signature__.bind(
            *args, **kwargs).arguments.items()]


if __name__ == '__main__':

    example_ad = {
        "car_manufacturer": "Toyota",
        "contact_phone": "0899999990",
        "car_fuel_type": "бензин",
        "related": {"username": 'foo', "barprop":1}
    }

    ad = CarAd(**example_ad)

    import json
    print(json.dumps(dict(ad.__dict__), default = lambda x: x.__dict__))
