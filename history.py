from weather_api_service import Weather
from weather_formatter import format_weather

from typing import Protocol
from datetime import datetime
from pathlib import Path

class WeatherStorage(Protocol):
    def save(self, weather: Weather) -> None:
        raise NotImplementedError

class PlainFileWeatherStorage:
    def __init__(self, file: Path):
        self._file = file

    def save(self, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = format_weather(weather)
        with open('history.txt', 'a') as f:
            f.write(f'{now}\n{formatted_weather}\n')

def save_weather(weather: Weather, storage: WeatherStorage) -> None:
    """Сохраняет погоду в хранилище"""
    storage.save(weather)