import requests
from flask import current_app

URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

AVAILABLE_LOCATIONS = [
    '12,Козловського,Львів',
    '100,Ряшівська,Львів',
    '16,Богданівська,Львів',
    '42,Джерельна,Львів',
    '2,Бойчука,Львів',
]


def pick_the_best(cars, answer: str):
    if answer == 'Рік':
        new = sorted(cars, key= lambda x: x.year, reverse=True)
    elif answer == 'Двигун':
        new = sorted(cars, key= lambda x: x.engine_capacity, reverse=True)
    else:
        new = sorted(cars, key= lambda x: x.rating, reverse=True)
    return new

def find_shortest_location(current: str):
    shortest = None
    for destination in AVAILABLE_LOCATIONS:
        r = requests.get(URL+ 'origins=' + current + '&destinations=' + destination + '&key=' + current_app.config['API_KEY'], timeout=10)
        print(r.json())
        try:
            value = r.json()['rows'][0]['elements'][0]['distance']['value']
        except KeyError:
            return None
        if shortest is None:
            shortest = destination, value
        else:
            if value < shortest[1]:
                shortest = destination, value

    return shortest[0]


