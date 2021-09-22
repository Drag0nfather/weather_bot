from dataclasses import dataclass


@dataclass
class DetailWeatherPartsForecastEntity:
    temp_min: int
    temp_max: int
    feels_like: int
    condition: str


@dataclass
class WeatherPartsForecastEntity:
    night: DetailWeatherPartsForecastEntity
    morning: DetailWeatherPartsForecastEntity
    day: DetailWeatherPartsForecastEntity
    evening: DetailWeatherPartsForecastEntity


@dataclass
class WeatherForecastEntity:
    parts: WeatherPartsForecastEntity


@dataclass
class WeatherFactEntity:
    temp: int
    feels_like: int
    condition: str


@dataclass
class WeatherEntity:
    fact: WeatherFactEntity
    forecasts: WeatherForecastEntity
