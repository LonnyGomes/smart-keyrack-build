#!/usr/bin/python3

from gpiozero import Button, Buzzer, MotionSensor
import time
from signal import pause
import requests
import os
from dotenv import load_dotenv
import asyncio

# internal module imports
from modules.OLEDDisplay import OLEDDisplay
from modules.OpenWeather import OpenWeather
from modules.NeoPixels import NeoPixels

load_dotenv()

OLED_SCREEN_TIMEOUT=15

# IFTTT Web hook parameters
IFTTT_BASE_WEBHOOK_URL="https://maker.ifttt.com/trigger/"
IFTTT_WEBHOOK_KEY=os.getenv('IFTTT_WEBHOOK_KEY')
IFTTT_EVENT_MOTION_DETECTED="key_motion_detected"
IFTTT_MOTION_DETECTED_URL=IFTTT_BASE_WEBHOOK_URL + \
    IFTTT_EVENT_MOTION_DETECTED + \
    "/with/key/" + \
    IFTTT_WEBHOOK_KEY

# OpenWeather parameters
OPEN_WEATHER_KEY=os.getenv('OPEN_WEATHER_KEY')
OPEN_WEATHER_CITY_ID=os.getenv('OPEN_WEATHER_CITY_ID')

# pin definitions
PIN_SOUND1=6
PIN_SOUND2=13
PIN_SOUND3=19
PIN_SOUND4=26
PIN_MOTION=12
PIN_WALLET_SWITCH=20

# NeoPixel defintions
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
PIN_NEOPIXELS = NeoPixels.D21
NEOPIXELS_NUM = 12
NEOPIXELS_ORDER = NeoPixels.GRBW
pixels = NeoPixels(
  PIN_NEOPIXELS, NEOPIXELS_NUM, NEOPIXELS_ORDER
)

# sensor input definitions
bz1 = Buzzer(PIN_SOUND1, initial_value=True)
bz2 = Buzzer(PIN_SOUND2, initial_value=True)
bz3 = Buzzer(PIN_SOUND3, initial_value=True)
bz4 = Buzzer(PIN_SOUND4, initial_value=True)

pir = MotionSensor(PIN_MOTION, threshold=0.5)

keyRackSwitch = Button(PIN_WALLET_SWITCH)

# init open weather API
ow = OpenWeather(OPEN_WEATHER_KEY)

# init OLED display
oled = OLEDDisplay()

# funciton definions
def onMotion(dev):
  print("Motion detected")

  if keyRackSwitch.is_pressed:
    bz1.off()
    pixels.animateOn((255, 0, 0, 0))
    time.sleep(2)
    bz1.on()
    # send notification off via IFTTT
    requests.post(IFTTT_MOTION_DETECTED_URL)

  weather = ow.getCurWeather(OPEN_WEATHER_CITY_ID)

  if weather['isSnow']:
    # show a snowflake if it's snowing
    asyncio.run(displaySnowflake())
  elif weather['isRain']:
    # show an umbrella if it's raining
    asyncio.run(displayUmbrella())
  else:
    # if not raining or snowing, show cur outisde temp
    temperature = round(weather['temp'])
    asyncio.run(displayWeather(temperature))

def onMotionStop(dev):
  print("Motion stopped")
  pixels.animateOff()
  time.sleep(10)

def keyRackSwitchDisengaged():
  print("key rack switch disengaged")
  # don't detect motion in these cases
  time.sleep(7)

def keyRackSwitchEngaged():
  print("key rack switch engaged")
  pixels.animateOn()
  bz2.off()
  time.sleep(3)
  bz2.on()
  pixels.animateOff()

async def displayWeather(temperatureVal):
  oled.showTemperature(temperatureVal)
  # keep the value on the screen for a set amount of time
  await asyncio.sleep(OLED_SCREEN_TIMEOUT)
  oled.clearScreen()

async def displaySnowflake():
  oled.drawSnowflake()
  # keep the value on the screen for a set amount of time
  await asyncio.sleep(OLED_SCREEN_TIMEOUT)
  oled.clearScreen()

async def displayUmbrella():
  oled.drawUmbrella()
  # keep the value on the screen for a set amount of time
  await asyncio.sleep(OLED_SCREEN_TIMEOUT)
  oled.clearScreen()

# handlers
pir.when_motion = onMotion
pir.when_no_motion = onMotionStop
keyRackSwitch.when_pressed = keyRackSwitchDisengaged
keyRackSwitch.when_released = keyRackSwitchEngaged

try:
  oled.clearScreen()
  pixels.animateOff()
  pause()
except (KeyboardInterrupt, SystemExit) as exErr:
  print("Closing down application")
finally:
  oled.clearScreen()
  pass
