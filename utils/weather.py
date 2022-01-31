import requests
import os
from dotenv import load_dotenv
from coordinates_stuff import split_coordinates_to_dict
from entity import WeatherEntity
from serializers import WeatherSerializer

load_dotenv()

weather_api_key = os.getenv('WEATHER_API_KEY')
weather_main_url = os.getenv('WEATHER_MAIN_URL')


class YandexWeatherConnector:
    headers = {
    }

    def __init__(self, token: str):
        self.headers['X-Yandex-API-Key'] = weather_api_key

    def get_weather_by_cors(self, coordinates):
        request = requests.get(
            weather_main_url,
            headers=self.headers,
            params=coordinates
        )
        request_json = request.json()
        serializer = WeatherSerializer().dump(request_json)
        entity = WeatherEntity(**serializer)
        return entity


if __name__ == '__main__':
    weather = YandexWeatherConnector(token=weather_api_key)
    # coordinates = get_coordinates_by_city('Москва')
    coordinates = '55.607329,37.51805'
    dict_coordinates = split_coordinates_to_dict(coordinates)
    print(weather.get_weather_by_cors(dict_coordinates))
