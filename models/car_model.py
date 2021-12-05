from functools import partial

from descriptors.typed import IntegerField, StringField
from descriptors.regex import PhoneField, RegexField
from descriptors.lookup_field import ModelField, OneOf

from models.base import BaseModel
from models.external_validators import IntegerHelpers, StringHelpers


class Address(BaseModel):

    x = partial(StringHelpers.is_in, values=['FO', "BG"])
    x.__qualname__ = 'foo'

    city = StringField()
    country_abbrev = RegexField("^[A-Z]{2}$", external_validators=[x])


class Person(BaseModel):
    name = StringField()
    contact_phone = PhoneField()
    gender = OneOf(["male", "female", "other"])
    address = ModelField(Address)
    age = IntegerField(external_validators=[IntegerHelpers.is_positive])
