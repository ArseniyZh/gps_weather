from gps_coordinates import Coordinates

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
from typing import Literal
import urllib.request
from urllib.error import URLError

import config

Celsius = float

class WeatherType(str, Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморось'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туманно'
    CLOUDS = 'Облачно'

@dataclass(frozen=True, slots=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates):
    """Делает запрос в OpenWeather API и возвращает его"""
    openweather_response = _get_openweather_response(
        longitude = coordinates.longitude, latitude = coordinates.latitude)

    weather = _parse_openweather_response(openweather_response)

    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(
        latitude = latitude, longitude = longitude)

    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise Exception('Ошибка API')


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise Exception('Ошибка API')

    return Weather(
        temperature = _parse_temperature(openweather_dict),
        weather_type = _parse_weather_type(openweather_dict),
        sunrise = _parse_sun_time(openweather_dict, "sunrise"),
        sunset = _parse_sun_time(openweather_dict, "sunset"),
        city = _parse_city(openweather_dict)
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise Exception('Ошибка API')

    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }

    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise Exception('Ошибка API')


def _parse_sun_time(
        openweather_dict: dict,
        time: Literal['sunrise'] or Literal['sunset']) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict['name']


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=55.7, longitude=37.6)))
