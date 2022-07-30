from gps_coordinates import get_gps_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather

from pathlib import Path
from history import PlainFileWeatherStorage, save_weather


def main():
    try:
        coordinates = get_gps_coordinates()
    except:
        print('Не смог корректно получить GPS координаты')
        exit(1)

    try:
        weather = get_weather(coordinates)
    except:
        print('Не смог корректно получить погоду в API сервиса погоды')
        exit(1)

    save_weather(
        weather, PlainFileWeatherStorage(Path.cwd())
    )

    print(format_weather(weather))

if __name__ == "__main__":
    main()