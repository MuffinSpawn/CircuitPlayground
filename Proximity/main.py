import analogio
import board
import busio
import digitalio
import math
import neopixel
import pulseio
import random
import time

def round(x):
    return int(x+0.5)

ir_pwm = pulseio.PWMOut(board.IR_TX, frequency=20000, duty_cycle=65536//4)
proximity = analogio.AnalogIn(board.IR_PROXIMITY)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0,0,0))
pixels.show()

# average resting proximity is 18982
# average solid on is about 19100
# max proximity is about 28200
min_proximity = 19100
max_proximity = 28200
amplitude = max_proximity - min_proximity
scale = 255 / amplitude

color_locked = False
rgb_selection = (0, 0, 0)
while True:
    # print('Proximity: {}'.format(proximity.value))
    prox = proximity.value
    print("{};".format(str(prox)))
    if prox > 19100:
        if not color_locked:
            color_locked = True
            rgb_selection = (random.randint(0,1),
                             random.randint(0,1),
                             random.randint(0,1))
            while not any(rgb_selection):
                rgb_selection = (random.randint(0,1),
                                 random.randint(0,1),
                                 random.randint(0,1))

        pixels.fill(((round((prox-min_proximity)*scale)+4)*rgb_selection[0],
                     (round((prox-min_proximity)*scale)+4)*rgb_selection[1],
                     (round((prox-min_proximity)*scale)+4)*rgb_selection[2]))
    else:
        color_locked = False
        pixels.fill((0, 0, 0))
    time.sleep(0.01)
