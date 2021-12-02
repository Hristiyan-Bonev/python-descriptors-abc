from resources.auto_manufacturers import MANUFACTURERS
from fields.lookup_field import DictLookupField
from fields.string_field import PhoneField


class CarAd:
    car_manufacturer = DictLookupField(lookup_dict=MANUFACTURERS)
    contact_phone = PhoneField(strict=False)


if __name__ == '__main__':
    ad = CarAd()
    ad.car_manufacturer = "Toyota"
    ad.contact_phone=""
