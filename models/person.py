from functools import partial, update_wrapper

from descriptors.typed import IntegerField, StringField
from descriptors.regex import PhoneField, RegexField
from descriptors.lookup_field import ModelField, OneOf

from models.base import BaseModel
from models.external_validators import IntegerHelpers, StringHelpers, func_with_args


class Address(BaseModel):
    city = StringField()
    country_abbrev = RegexField("^[A-Z]{2}$", external_validators=[func_with_args(StringHelpers.is_in, values=["BG", "DE"])])


class Person(BaseModel):
    name = StringField()
    contact_phone = PhoneField()
    gender = OneOf(["male", "female", "other"])
    address = ModelField(Address)
    age = IntegerField(external_validators=[IntegerHelpers.is_positive])
