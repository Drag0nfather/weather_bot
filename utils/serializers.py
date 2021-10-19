from marshmallow import Schema, fields


class WeatherPartsForecastSerializer(Schema):
    part_name = fields.String()
    temp_min = fields.Integer()
    temp_max = fields.Integer()
    feels_like = fields.Integer()
    condition = fields.String()


class WeatherForecastSerializer(Schema):
    sunrise = fields.String()
    sunset = fields.String()
    parts = fields.List(fields.Nested(WeatherPartsForecastSerializer))


class WeatherFactSerializer(Schema):
    temp = fields.Integer()
    feels_like = fields.Integer()
    condition = fields.String()


class WeatherSerializer(Schema):
    fact = fields.Nested(WeatherFactSerializer)
    forecast = fields.Nested(WeatherForecastSerializer)
