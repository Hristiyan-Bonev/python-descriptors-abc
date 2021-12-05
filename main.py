from models.car_model import CarAd

if __name__ == '__main__':

    example_ad = {
        "car_manufacturer": "Toyota",
        "contact_phone": "0899999990",
        "car_fuel_type": "бензин",
        "related": {"username": 2, "location":{"lat": 5, "long": 3}},
        "related_tags": {"tag_type": "broken", "tag_value":1}
    }

    ad = CarAd(**example_ad)
    from pprint import pprint as pp
    pp([x for x in ad._errors])
    import json
    # import ipdb;ipdb.set_trace()
    print(json.dumps(dict(ad.__dict__), default = lambda x: x.__dict__))
