from entity import WeatherEntity


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
    temperature = entity.fact['temp']
    sunset = entity.forecast['sunset']
    sunrise = entity.forecast['sunrise']
    condition = entity.fact['condition']
    feels_like = entity.fact['feels_like']
    string = f'За окном {CONDITION_DICT[condition]}, ощущается как {feels_like} \nТемпература: {temperature} \nРассвет: {sunrise} Закат: {sunset} '
    return string
