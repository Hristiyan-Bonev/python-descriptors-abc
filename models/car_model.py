from models.base import BaseModel

from descriptors.typed import IntegerField, StringField
from descriptors.regex import PhoneField
from descriptors.lookup_field import ModelField, OneOf
from models.external_validators import IntegerHelpers
from resources.auto_manufacturers import MANUFACTURERS


def is_even(value):
    if value % 2 == 0:
        raise ValueError("Must be positive")


class Location(BaseModel):
    long = IntegerField(external_validators=[IntegerHelpers.is_even, IntegerHelpers.is_positive])
    lat = IntegerField()


class Tag(BaseModel):
    tag_type = OneOf(["broken", "new"])
    tag_value = IntegerField()


class Person(BaseModel):
    username = StringField()
    address = StringField(default_value="F")
    location = ModelField(Location)


class CarAd(BaseModel):
    car_manufacturer = OneOf(lookup_values=MANUFACTURERS, required=True)
    contact_phone = PhoneField(required=True)
    car_fuel_type = OneOf(["Дизел", "Бензин", "Газ/Бензин",
                          "Метан/Бензин", "Хибрид"], case_sensitive=False)
    related = ModelField(Person)
    related_tags = ModelField(Tag)
