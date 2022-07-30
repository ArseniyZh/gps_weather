OPENWEATHER_API = '0aae40e6b060426c91c07d770e1092ef'
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&"
    "units=metric"
)

#print(OPENWEATHER_URL.format(latitude = 10, longitude = 20))