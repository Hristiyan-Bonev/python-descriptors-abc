import json
from models.car_model import CarAd

from pprint import pprint as pp


if __name__ == '__main__':

    example_ads = [
        # {
        #     "car_manufacturer": "AyToyota",
        #     "contact_phone": "089999a9990",
        #     "car_fuel_type": "бенз3ин",
        #     "related": {"username": 2, "location": {"lat": 5, "long": 4}},
        #     "related_tags": {"tag_type": "broken", "tag_value": 1}
        # }, 
        {
            # "car_manufacturer": "AyToyota",
            "contact_phone": "089999a9990",
            "car_fuel_type": "бенз3ин",
            "related": {"username": "Goo", "location": {"lat": 0, "long": -121}},
            "related_tags": {"tag_type": "foooo", "tag_value": 1}
        }
    ]

    for ad in example_ads:
        foo = CarAd(**ad)
        pp(json.loads(json.dumps(foo.__dict__, default=lambda x: x.__dict__)))