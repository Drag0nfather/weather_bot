import json
from typing import Dict

f = open('./json_obj/cities_and_cors.json', )
cities_data = json.load(f)


def get_coordinates_by_city(city: str) -> str:
    """
    Возвращает координаты города по названию
    """
    # TODO сюда рейз ошибки, если город не найден, или неправильно введен
    # TODO засунуть сюда проверку на маленькую первую букву, если да - то upperCase
    for city_data in cities_data:
        if city_data['name'] == city:
            return city_data['coordinates']


def split_coordinates_to_dict(coordinates: str) -> Dict:
    """
    Возвращает координаты в виде словаря
    """
    lat, lon = coordinates.split(',')
    coordinates_dict = {
        'lat': lat,
        'lon': lon
    }
    return coordinates_dict


if __name__ == '__main__':
    coordinates = get_coordinates_by_city('Лобня')
    print(coordinates)
    print(split_coordinates_to_dict(coordinates))
