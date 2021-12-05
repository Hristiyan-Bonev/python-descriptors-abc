import inspect
from functools import partialmethod

from descriptors.base import Field



class InitMeta(type):
    def __new__(cls, bases, dicts, class_attrs):
        class_obj = super().__new__(cls, bases, dicts, class_attrs)

        init_params = []
        for attr_name, attr in class_obj.__dict__.items():
            if isinstance(attr, Field):
                param = inspect.Parameter(attr_name, inspect.Parameter.POSITIONAL_OR_KEYWORD, default=attr.__dict__.get(
                    'default_value', inspect.Parameter.empty))
                init_params.append(param)

        setattr(class_obj, '__signature__',
                inspect.Signature(parameters=init_params))

        return class_obj


class BaseModel(metaclass=InitMeta):
    def __init__(self, error_container=None, *args, **kwargs):

        self.errors_list = error_container or []

        sig = self.__signature__.bind(*args, **kwargs)
        sig.apply_defaults()
        for attr_name, attr in sig.arguments.items():
            try:
                setattr(self, attr_name, attr)
            except (ValueError, TypeError,) as exc:
                self.errors_list.append(exc)