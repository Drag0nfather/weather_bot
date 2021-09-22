import requests
from coordinates_stuff import get_coordinates_by_city, split_coordinates_to_dict
from utils.entity import WeatherEntity
from utils.serializers import WeatherSerializer

WEATHER_API_KEY = '6250b558-14b3-4617-a2ed-36231e94773c'
WEATHER_MAIN_URL = 'https://api.weather.yandex.ru/v2/forecast'


class YandexWeatherConnector:

    headers = {
    }

    def __init__(self, token: str):
        self.headers['X-Yandex-API-Key'] = WEATHER_API_KEY

    def get_weather_by_cors(self, coordinates):
        request = requests.get(
            WEATHER_MAIN_URL,
            headers=self.headers,
            params=coordinates
        )
        request_json = request.json()
        serializer = WeatherSerializer().dump(request_json)
        entity = WeatherEntity(**serializer)
        return entity


if __name__ == '__main__':
    weather = YandexWeatherConnector(token=WEATHER_API_KEY)
    coordinates = get_coordinates_by_city('Малаховка')
    dict_coordinates = split_coordinates_to_dict(coordinates)
    print(weather.get_weather_by_cors(dict_coordinates))
