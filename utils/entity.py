from dataclasses import dataclass

@dataclass
class WeatherPartsForecastEntity:
    temp_min: int
    temp_max: int
    feels_like: int
    condition: str
    part_name: str


@dataclass
class WeatherForecastEntity:
    sunrise: str
    sunset: str
    parts: WeatherPartsForecastEntity


@dataclass
class WeatherFactEntity:
    temp: int
    condition: str
    feels_like: int


@dataclass
class WeatherEntity:
    fact: WeatherFactEntity
    forecast: WeatherForecastEntity
