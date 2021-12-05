import inspect
from functools import partialmethod

from descriptors.base import Field


def _custom_init(self, error_container, *args, **kwargs):

    sig = self.__signature__.bind(*args, **kwargs)
    sig.apply_defaults()
    for attr_name, attr in sig.arguments.items():
        try:
            setattr(self, attr_name, attr)
        except (ValueError, TypeError,) as exc:
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

        setattr(class_obj, '__signature__',
                inspect.Signature(parameters=init_params))

        setattr(class_obj, '__init__', partialmethod(
            _custom_init, error_container=errors_container))
        setattr(class_obj, '_errors', errors_container)

        return class_obj


class BaseModel(metaclass=InitMeta):
    pass
