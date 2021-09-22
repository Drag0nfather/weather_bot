from marshmallow import Schema, fields


class DetailWeatherPartsForecastSerializer(Schema):
    temp_min = fields.Integer()
    temp_max = fields.Integer()
    feels_like = fields.Integer()
    condition = fields.String()


class WeatherPartsForecastSerializer(Schema):
    night = fields.Nested(DetailWeatherPartsForecastSerializer)
    morning = fields.Nested(DetailWeatherPartsForecastSerializer)
    day = fields.Nested(DetailWeatherPartsForecastSerializer)
    evening = fields.Nested(DetailWeatherPartsForecastSerializer)


class WeatherForecastSerializer(Schema):
    parts = fields.Nested(WeatherPartsForecastSerializer)


class WeatherFactSerializer(Schema):
    temp = fields.Integer()
    feels_like = fields.Integer()
    condition = fields.String()


class WeatherSerializer(Schema):
    fact = fields.Nested(WeatherFactSerializer)
    forecasts = fields.List(fields.Nested(WeatherForecastSerializer))
