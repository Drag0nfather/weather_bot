import json
import os
from typing import Dict
from pathlib import Path

path_to_json_folder = os.path.join(Path(os.getcwd()), 'json_obj')
f = open(os.path.join(path_to_json_folder, 'cities_and_cors.json'), )
cities_data = json.load(f)


def get_coordinates_by_city(city: str) -> str:
    """
    Возвращает координаты города по названию
    """
    for city_data in cities_data:
        if city_data['name'] == city.capitalize():
            return city_data['coordinates']


def split_coordinates_to_dict(coordinates: str, flag=False) -> Dict:
    """
    Возвращает координаты в виде словаря
    """
    if flag == False:
        lat, lon = coordinates.split(',')
        coordinates_dict = {
            'lat': lat,
            'lon': lon
        }
    else:
        coordinates_dict = {
            'lat': coordinates[0],
            'lon': coordinates[1]
        }
    return coordinates_dict
