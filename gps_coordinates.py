from dataclasses import dataclass
from subprocess import Popen, PIPE
import geocoder

@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float

def get_gps_coordinates() -> Coordinates:
    """Возвращает координаты компьютера"""
    coords = geocoder.ip('me').latlng
    latitude = coords[0]
    longitude = coords[1]

    return Coordinates(longitude=longitude, latitude=latitude)

if __name__ == "__main__":
    print(get_gps_coordinates())