import requests
from cachetools import TTLCache

OW_BASE_URL="https://api.openweathermap.org/data/2.5/"
CUR_WEATHER_KEY = "curWeather"

class OpenWeather:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.cache = TTLCache(maxsize=10, ttl=300)
        
    def getCurWeather(self, cityId):
        url = "{baseUrl}/weather?id={cityId}&appid={apiKey}&units=imperial"\
                .format(baseUrl=OW_BASE_URL,\
                        cityId = cityId,\
                        apiKey = self.apiKey)
        try:
            weather = self.cache[CUR_WEATHER_KEY]
        except (KeyError):
            # if key does not exist or expired, grab from API
            results = requests.get(url)
            weather = results.json()['main']
            self.cache[CUR_WEATHER_KEY] = weather

        return weather

