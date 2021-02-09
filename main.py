#!/usr/bin/python3

from gpiozero import Button, Buzzer, MotionSensor
import time
import board
import neopixel
from signal import pause
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# IFTTT Web hook parameters
IFTTT_BASE_WEBHOOK_URL="https://maker.ifttt.com/trigger/"
IFTTT_WEBHOOK_KEY=os.getenv('IFTTT_WEBHOOK_KEY')
IFTTT_EVENT_MOTION_DETECTED="key_motion_detected"
IFTTT_MOTION_DETECTED_URL=IFTTT_BASE_WEBHOOK_URL + \
        IFTTT_EVENT_MOTION_DETECTED + \
        "/with/key/" + \
        IFTTT_WEBHOOK_KEY

# pin definitions
PIN_SOUND1=6
PIN_SOUND2=13
PIN_SOUND3=19
PIN_SOUND4=26
PIN_MOTION=12
PIN_WALLET_SWITCH=20
PIN_NEOPIXELS = board.D21 # NeoPixels must be connected to D10, D12, D18 or D21 to work.

# NeoPixel defintions
NEOPIXELS_NUM = 12
NEOPIXELS_ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(
    PIN_NEOPIXELS, NEOPIXELS_NUM, brightness=1, auto_write=False, pixel_order=NEOPIXELS_ORDER
)

# sensor input definitions
bz1 = Buzzer(PIN_SOUND1, initial_value=True)
bz2 = Buzzer(PIN_SOUND2, initial_value=True)
bz3 = Buzzer(PIN_SOUND3, initial_value=True)
bz4 = Buzzer(PIN_SOUND4, initial_value=True)

pir = MotionSensor(PIN_MOTION, threshold=0.5)

walletSwitch = Button(PIN_WALLET_SWITCH)

# funciton definions
def pixelsTurnOff(pixelCount):
    for pixelIdx in reversed(range(pixelCount)):
        pixels[pixelIdx] = (0, 0, 0, 0)
        pixels.show()
        time.sleep(0.05)

def pixelsAnimate(pixelCount, rgbw = (0, 0, 0, 255)):
    for pixelIdx in range(pixelCount):
        pixels[pixelIdx] = rgbw
        pixels.show()
        time.sleep(0.05)

def onMotion(dev):
    print("Motion detected")
    if walletSwitch.is_pressed:
        bz1.off()
        pixelsAnimate(NEOPIXELS_NUM, (255, 0, 0, 0))
        time.sleep(2)
        bz1.on()
        # send notification off via IFTTT
        requests.post(IFTTT_MOTION_DETECTED_URL)

def onMotionStop(dev):
    print("Motion stopped")
    pixelsTurnOff(NEOPIXELS_NUM)
    time.sleep(10)

def walletSwitchDisengaged():
    print("wallet switch disengaged")
    # don't detect motion in these cases
    time.sleep(7)

def walletSwitchEngaged():
    print("wallet switch engaged")
    pixelsAnimate(NEOPIXELS_NUM)
    bz2.off()
    time.sleep(3)
    bz2.on()
    pixelsTurnOff(NEOPIXELS_NUM)

# handlers
pir.when_motion = onMotion
pir.when_no_motion = onMotionStop
walletSwitch.when_pressed = walletSwitchDisengaged
walletSwitch.when_released = walletSwitchEngaged

try:
    pixelsTurnOff(NEOPIXELS_NUM)
    pause()
finally:
    pass
