import json
from models.car_model import Person

from pprint import pprint as pp
import logging

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':

    data = json.load(open('resources/person.json'))

    out = []

    for d in data:
        out.append(Person(**d))

    
    outt = json.loads(json.dumps(out, default = lambda x: x.__dict__))
    
    # import  csv
    # with open('dict.csv', 'w') as csv_file:  
    #     writer = csv.DictWriter(csv_file, fieldnames=outt[0].keys())
    #     writer.writeheader()
    #     for item in outt:
    #         writer.writerow(item)
    with open('out.json', 'w') as out_file:

        out_file.write(json.dumps(outt, indent=4, sort_keys=True))