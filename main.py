from ast import Str

from _pytest.assertion import install_importhook
from resources.auto_manufacturers import MANUFACTURERS
from fields.lookup_field import NestedField, OneOf, DictField,ObjectContainer
from fields.string_field import IntegerField, PhoneField, StringField
from fields.base_field import Field

import inspect
from functools import partial, partialmethod
def _custom_init(self, error_container, *args, **kwargs):

    sig = self.__signature__.bind(*args,**kwargs)
    sig.apply_defaults()
    for attr_name, attr in sig.arguments.items():
        try: 
            setattr(self, attr_name, attr)
        except (ValueError,TypeError,) as exc:
            error_container.append(exc)            


errors_container = []


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

        setattr(class_obj, '__init__', partialmethod(_custom_init,error_container=errors_container))
        setattr(class_obj, '_errors', errors_container)
        
        return class_obj


class BaseModel(metaclass=InitMeta):
    pass

class Bar(BaseModel):
    long = IntegerField()
    lat = IntegerField()

class Tag(BaseModel):
    tag_type = OneOf(["broken", "new"])
    tag_value = IntegerField()

class Foo(BaseModel):
    username = StringField()
    address = StringField(default_value="F")
    location = NestedField(Bar)



class CarAd(BaseModel):
    car_manufacturer = OneOf(lookup_values=MANUFACTURERS, required=True)
    contact_phone = PhoneField(required=True)
    car_fuel_type = OneOf(["Дизел", "Бензин", "Газ/Бензин",
                          "Метан/Бензин", "Хибрид"], case_sensitive=False)
    related = NestedField(Foo) 
    related_tags = ObjectContainer(Tag)

    # def __init__(self, *args, **kwargs) -> None:
    #     [setattr(self, name, val) for name, val in self.__signature__.bind(
    #         *args, **kwargs).arguments.items()]


if __name__ == '__main__':

    example_ad = {
        "car_manufacturer": "Toyota",
        "contact_phone": "0899999990",
        "car_fuel_type": "бензин",
        "related": {"username": 'foo', "location":{"lat": 5, "long": 3}},
        "related_tags": [{"tag_type": "broken", "tag_value":1}]
    }

    ad = CarAd(**example_ad)
    from pprint import pprint as pp
    pp([x for x in ad._errors])
    import json
    # import ipdb;ipdb.set_trace()
    print(json.dumps(dict(ad.__dict__), default = lambda x: x.__dict__))
