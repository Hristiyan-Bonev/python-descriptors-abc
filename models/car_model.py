from models.base import BaseModel

from descriptors.typed import IntegerField, StringField
from descriptors.regex import PhoneField
from descriptors.lookup_field import ModelField, OneOf

from resources.auto_manufacturers import MANUFACTURERS


class Bar(BaseModel):
    long = IntegerField()
    lat = IntegerField()


class Tag(BaseModel):
    tag_type = OneOf(["broken", "new"])
    tag_value = IntegerField()


class Foo(BaseModel):
    username = StringField(required=True)
    address = StringField(default_value="F")
    location = ModelField(Bar)


class CarAd(BaseModel):
    car_manufacturer = OneOf(lookup_values=MANUFACTURERS, required=True)
    contact_phone = PhoneField(required=True)
    car_fuel_type = OneOf(["Дизел", "Бензин", "Газ/Бензин",
                          "Метан/Бензин", "Хибрид"], case_sensitive=False)
    related = ModelField(Foo)
    related_tags = ModelField(Tag)
