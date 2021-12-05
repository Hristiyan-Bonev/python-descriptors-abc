from models.base import BaseModel

from descriptors.typed import IntegerField, StringField, ValidatorFunction
from descriptors.regex import PhoneField
from descriptors.lookup_field import ModelField, OneOf

from resources.auto_manufacturers import MANUFACTURERS


class Location(BaseModel):
    long = IntegerField(additional_validators=[ValidatorFunction(lambda x: x>0, "The number must be > 0"), lambda x: x])
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
