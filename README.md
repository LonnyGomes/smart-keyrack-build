# Smart Keyrack Build

Source code for smart key rack that is run on a raspberry pi zero

## Installation

Install dotenv 

```bash
sudo -H pip3 install -U python-dotenv
sudo -H pip3 install -U cachetools
```

Copy `env-sample` to `.env` and then edit the `.env` file

Add the `IFTTT_WEBHOOK_KEY` value to the `.env` file.  The value can be retrieved by clicking on the `Documentation` link on the [IFTTT Webhooks page](https://ifttt.com/maker_webhooks).

Create an [https://openweather.org](https://openweathermap.org/current#data) account and API key. Store the API key in the `OPEN_WEATHER_KEY` variable.

Find your city listed in the [city.list.json.gz](http://bulk.openweathermap.org/sample/city.list.json.gz) and added enter it as the `OPEN_WEATHER_CITY_ID` value.

## Resources

- [Installing NeoPixel on a pi](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [image2cpp](https://javl.github.io/image2cpp/)
- [SparkFun OLED screen](https://www.sparkfun.com/products/13003)
- [OpenWeather API](https://openweathermap.org/current#data)
