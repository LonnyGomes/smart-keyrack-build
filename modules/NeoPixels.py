#!/usr/bin/python3

import board
import neopixel
import time

class NeoPixels:
  # color order configurations
  GRBW = neopixel.GRBW
  RGBW = neopixel.RGBW
  RGB = neopixel.RGB
  GRB = neopixel.GRB

  # available PIN layouts
  D10 = board.D10
  D12 = board.D12
  D18 = board.D18
  D21 = board.D21

  # NeoPixels must be connected to D10, D12, D18 or D21 to work.
  def __init__(self, pixelPin, pixelCount, order):
    self.pixelCount = pixelCount
    self.pixels = neopixel.NeoPixel(\
      pixelPin, pixelCount, brightness=1,\
      auto_write=False, pixel_order=order\
    )

  # funciton definions
  def animateOff(self):
    for pixelIdx in reversed(range(self.pixelCount)):
      self.pixels[pixelIdx] = (0, 0, 0, 0)
      self.pixels.show()
      time.sleep(0.05)

  def animateOn(self, rgbw = (0, 0, 0, 255)):
    for pixelIdx in range(self.pixelCount):
      self.pixels[pixelIdx] = rgbw
      self.pixels.show()
      time.sleep(0.05)

if __name__ == '__main__':
  try:
    # remove after testing
    np = NeoPixels(NeoPixels.D21, 12, NeoPixels.GRBW)
    np.animateOn()
    time.sleep(5)
    np.animateOff()
  except (KeyboardInterrupt, SystemExit) as exErr:
    print("Closing down application")
  finally:
    pass
