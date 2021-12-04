from resources.auto_manufacturers import MANUFACTURERS
from fields.lookup_field import OneOf
from fields.string_field import PhoneField
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
        _mapping_fields = {k: v for k, v in class_obj.__dict__.items(
        ) if isinstance(v, Field) and v.__dict__.get('default')}

        init_params = []

        for attr_name, attr in class_obj.__dict__.items():
            if isinstance(attr, Field):
                param = inspect.Parameter(attr_name, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=attr.__dict__.get(
                    'default_value', inspect.Parameter.empty))
                init_params.append(param)

        obj_sig = inspect.Signature(parameters=init_params)
        setattr(class_obj, '__signature__', obj_sig)

        setattr(class_obj, '__init__', _custom_init)
        return class_obj


class CarAd(metaclass=InitMeta):
    car_manufacturer = OneOf(lookup_values=MANUFACTURERS)
    contact_phone = PhoneField(required=True)
    car_fuel_type = OneOf(["Дизел", "Бензин", "Газ/Бензин",
                          "Метан/Бензин", "Хибрид"], case_sensitive=True)

    def __init__(self, *args, **kwargs) -> None:
        [setattr(self, name, val) for name, val in self.__signature__.bind(
            *args, **kwargs).arguments.items()]


if __name__ == '__main__':

    example_ad = {
        "car_manufacturer": "Toyota",
        "contact_phone": "0899999990",
        "car_fuel_type": "бензин"
    }

    ad = CarAd(**example_ad)

    print(dict(ad.__dict__))
