#!/usr/bin/python3

from gpiozero import Buzzer,MotionSensor
from signal import pause

# pin definitions
PIN_SOUND1=8
PIN_SOUND2=11
PIN_SOUND3=9
PIN_SOUND4=10
PIN_MOTION=7

# sensor input definitions
bz1 = Buzzer(PIN_SOUND1, initial_value=True)
bz2 = Buzzer(PIN_SOUND2, initial_value=True)
bz3 = Buzzer(PIN_SOUND3, initial_value=True)
bz4 = Buzzer(PIN_SOUND4, initial_value=True)

pir = MotionSensor(PIN_MOTION, threshold=0.5)

#bz1.off()

# funciton definions
def onMotion(dev):
    print("Motion detected")

# handlers
pir.when_motion = onMotion

pause()
