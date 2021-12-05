from models.base import BaseModel

from descriptors.typed import IntegerField, StringField
from descriptors.regex import PhoneField, RegexField

from descriptors.lookup_field import ModelField, OneOf

from models.external_validators import IntegerHelpers, StringHelpers
from functools import partial, update_wrapper

class Address(BaseModel):

    x = partial(StringHelpers.is_in, values=['FO', "BG"])
    x.__qualname__='foo'

    city = StringField()
    country_abbrev = RegexField("^[A-Z]{2}$", external_validators=[x])


class Person(BaseModel):
    name = StringField(required=True)
    contact_phone = PhoneField(required=True)
    gender = OneOf(["male", "female", "other"], case_sensitive=False)
    address = ModelField(Address)
    age = IntegerField(external_validators=[IntegerHelpers.is_positive])