from coordinates_stuff import get_coordinates_by_city, split_coordinates_to_dict
from entity import WeatherEntity
from weather import YandexWeatherConnector, weather_api_key


CONDITION_DICT = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно-сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом',
}


def create_output_message(entity: WeatherEntity) -> str:
    condition = entity.fact['condition']
    feels_like = entity.fact['feels_like']
    string = f'За окном {CONDITION_DICT[condition]}, ощущается как {feels_like}'
    return string


if __name__ == '__main__':
    weather = YandexWeatherConnector(token=weather_api_key)
    coordinates = get_coordinates_by_city('Малаховка')
    dict_coordinates = split_coordinates_to_dict(coordinates)
    entity = weather.get_weather_by_cors(dict_coordinates)
    print(create_output_message(entity))
