import requests
from cachetools import TTLCache
import math

OW_BASE_URL="https://api.openweathermap.org/data/2.5/"
CUR_WEATHER_KEY = "curWeather"
WEATHER_KEY = "weather"
WEATHER_ID_KEY = "weatherId"

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
      weatherData = results.json()['weather']
      weather = results.json()['main']
      weather[WEATHER_KEY] = weatherData[0]['main']
      weather[WEATHER_ID_KEY] = weatherData[0]['id']
      weather['isSnow'] = False
      weather['isRain'] = False

      self.cache[CUR_WEATHER_KEY] = weather

      # check weather type
      # https://openweathermap.org/weather-conditions
      # 5XX codes are rain and 6XX codes are snow
      if math.floor(weather[WEATHER_ID_KEY] / 100) == 5:
        weather['isRain'] = True
      elif math.floor(weather[WEATHER_ID_KEY] / 100) == 6:
        weather['isSnow'] = True

    return weather

if __name__ == '__main__':
  print("TODO")
