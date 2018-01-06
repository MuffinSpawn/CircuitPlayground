import analogio
import board
import busio
import digitalio
import math
import neopixel
import pulseio
import random
import time

import adafruit_lis3dh

def round(x):
    return int(x+0.5)
# ['A0', 'SPEAKER', 'A1', 'A2', 'A3', 'A4', 'SCL', 'A5', 'SDA', 'A6', 'RX', 'A7', 'TX', 'LIGHT', 'A8', 'TEMPERATURE',
#  'A9', 'BUTTON_A', 'D4', 'BUTTON_B', 'D5', 'SLIDE_SWITCH', 'D7', 'NEOPIXEL', 'D8', 'D13', 'REMOTEIN', 'IR_RX',
#  'REMOTEOUT', 'IR_TX', 'IR_PROXIMITY', 'MICROPHONE_CLOCK', 'MICROPHONE_DATA', 'ACCELEROMETER_INTERRUPT',
#  'ACCELEROMETER_SDA', 'ACCELEROMETER_SCL', 'SPEAKER_ENABLE', 'SCK', 'MOSI', 'MISO', 'FLASH_CS']

class State():
    UNKNOWN = 0
    READY = 1
    LOCKED = 2
    FLAT = 3
    INVERTED = 4
    TILTED_LEFT = 5
    TILTED_RIGHT = 6
    TILTED_FORWARD = 7
    TILTED_BACKWARD = 8
    INVERTED_TILTED_LEFT = 9
    INVERTED_TILTED_RIGHT = 10
    INVERTED_TILTED_FORWARD = 11
    INVERTED_TILTED_BACKWARD = 12


i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

ir_pwm = pulseio.PWMOut(board.IR_TX, frequency=20000, duty_cycle=65536//4)
proximity = analogio.AnalogIn(board.IR_PROXIMITY)

'''
total = 0
for i in range(max_color):
    x, y, z = lis3dh.acceleration
    total += y
average = total / max_color.0
print('Average: {} m/s^2'.format(average))
'''

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0,0,0))
pixels.show()
'''
slide_switch = digitalio.DigitalInOut(board.D7)
slide_switch.direction = digitalio.Direction.INPUT
'''

# average resting proximity is 18982
# average solid on is about 19100
# max proximity is about 28200
min_proximity = 19100
max_proximity = 29800
amplitude = max_proximity - min_proximity
scale = 255 / amplitude

color_locked = False
rgb_selection = (0, 0, 0)
state = State.UNKNOWN
while True:
    x, y, z = lis3dh.acceleration  # m/s^2

    # x: {-9.17405,  9.71178}
    cal_x = (x  - 0.268867) / 9.44291
    # y: { -9.95718, 9.56898}
    cal_y = (y + 0.194099) / 9.76308
    # z: {-9.77008, 9.9808} --> z' = (z - 0.105363) / 9.87543
    cal_z = (z - 0.105363) / 9.7
    print('x = {}G, y = {}G, z = {}G'.format(cal_x, cal_y, cal_z))
    prox = proximity.value
    # print("{};".format(str(prox)))
    if state == State.UNKNOWN:
        pixels.fill((0, 0, 0))
        if prox > 20000:
            state = State.READY
        else:
            state = State.UNKNOWN
    elif state == State.READY:
        pixels.fill((0, 0, 0))
        if prox < 20000:
            state = State.UNKNOWN
        if abs(cal_x) <= 0.2 and cal_y >= 0.75 and cal_z <= 0.65:
            state = State.LOCKED
    elif state == State.LOCKED:
        pixels.fill((100, 100, 100))
        if prox < 20000 and abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.FLAT:
        pixels.fill((0, 0, 255))  # blue
        if prox > 20000:
            state = State.READY
        elif abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z <= -0.8:
            state = State.INVERTED
        elif cal_x <= -0.8 and abs(cal_y) <= 0.4 and cal_z <= 0.4:
            state = State.TILTED_LEFT
        elif abs(cal_x) <= 0.2 and cal_y >= 0.75 and cal_z <= 0.65:
            state - State.TILTED_FORWARD
        elif cal_x >= 0.8 and abs(cal_y) <= 0.4 and cal_z <= 0.4:
            state = State.TILTED_RIGHT
        elif abs(cal_x) <= 0.2 and cal_y <= -0.75 and cal_z <= 0.65:
            state - State.TILTED_BACKWARD
    elif state == State.INVERTED:
        pixels.fill((0, 255, 0))
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
        elif cal_x <= -0.8 and abs(cal_y) <= 0.4 and cal_z <= 0.4:
            state = State.INVERTED_TILTED_LEFT
        elif abs(cal_x) <= 0.2 and cal_y >= 0.75 and cal_z <= 0.65:
            state - State.INVERTED_TILTED_FORWARD
        elif cal_x >= 0.8 and abs(cal_y) <= 0.4 and cal_z <= 0.4:
            state = State.INVERTED_TILTED_RIGHT
        elif abs(cal_x) <= 0.2 and cal_y <= -0.75 and cal_z <= 0.65:
            state - State.INVERTED_TILTED_BACKWARD
    elif state == State.TILTED_LEFT:
        pixels.fill((85, 170, 255))
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.TILTED_RIGHT:
        pixels.fill((255, 170, 85))
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.TILTED_FORWARD:
        pixels.fill((0, 170, 255))  # red
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.TILTED_BACKWARD:
        pixels.fill((0, 85, 255))  # green
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.INVERTED_TILTED_LEFT:
        pixels.fill((85, 255, 170))
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.INVERTED_TILTED_RIGHT:
        pixels.fill((255, 85, 170))
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.INVERTED_TILTED_FORWARD:
        pixels.fill((0, 255, 170))  # red
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT
    elif state == State.INVERTED_TILTED_BACKWARD:
        pixels.fill((0, 255, 85))  # green
        if abs(cal_x) < 0.5 and abs(cal_y) < 0.5 and cal_z >= 0.8:
            state = State.FLAT

'''

pixel_angles = [-math.pi/3, -math.pi/6, 0.0, math.pi/6, math.pi/3,
                2*math.pi/3, 5*math.pi/6, math.pi, -5*math.pi/6, -2*math.pi/3]
pixel_upper_limits = [t + math.pi/12 for t in pixel_angles]
pixel_upper_limits[7] = -math.pi*11/12
pixel_lower_limits = [t - math.pi/12 for t in pixel_angles]
max_color = 50
while True:
    x, y, z = lis3dh.acceleration  # m/s^2

    # x: {-9.17405,  9.71178}
    cal_x = (x  - 0.268867) / 9.44291
    # y: { -9.95718, 9.56898}
    cal_y = (y + 0.194099) / 9.76308
    # z: {-9.77008, 9.9808} --> z' = (z - 0.105363) / 9.87543
    cal_z = (z - 0.105363) / 9.7
    #print('x = {}G, y = {}G, z = {}G'.format(cal_x, cal_y, cal_z))
    time.sleep(0.1)

    if (cal_z >= 0):
        pixels.fill((0, int(cal_z * max_color), 0))
    else:
        pixels.fill((int(-cal_z * max_color), 0, 0))

    pixel_index = 0
    theta = math.atan2(cal_y, cal_x)
    #print('x-y angle: {} rad'.format(theta))
    if theta >= pixel_lower_limits[7] or theta < pixel_upper_limits[7]:
        pixels[7] = (max_color, max_color, max_color)
    elif theta >= pixel_upper_limits[4] and theta < pixel_lower_limits[5]:
        pixels[4] = (max_color, max_color, max_color)
        pixels[5] = (max_color, max_color, max_color)
    elif theta >= pixel_upper_limits[9] and theta < pixel_lower_limits[0]:
        pixels[0] = (max_color, max_color, max_color)
        pixels[9] = (max_color, max_color, max_color)
    else:
        for index in range(len(pixel_angles)):
            theta_upper = pixel_upper_limits[index]
            theta_lower = pixel_lower_limits[index]
            if theta >= theta_lower and theta < theta_upper:
                index
                break
        pixels[index] = (max_color, max_color, max_color)
'''

'''
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT
while True:
    led.value = not led.value
    time.sleep(0.5)
'''

'''
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0,0,0))
pixels.show()

while True:
    r = random.randrange(255)
    g = random.randrange(255)
    b = random.randrange(255)
    for index in range(5):
        pixels[index] = ((r, g, b))
        pixels[9-index] = ((r, g, b))
        time.sleep(0.050)
    time.sleep(0.5)

    for index in range(5, -1, -1):
        pixels[index] = ((0, 0, 0))
        pixels[9-index] = ((0, 0, 0))
        time.sleep(0.050)
    time.sleep(0.2)
'''

'''
step = 20
while True:
	for r in range(0, 255, step):
		for g in range(0, 255, step):
			for b in range(0, 255, step):
				pixels.fill((r, g, b))
			for b in range(255, 0, -step):
				pixels.fill((r, g, b))
		for g in range(255, 0, -step):
			pixels.fill((r, g, b))
			for b in range(0, 255, step):
				pixels.fill((r, g, b))
			for b in range(255, 0, -step):
				pixels.fill((r, g, b))
	for r in range(255, 0, -step):
		for g in range(0, 255, step):
			for b in range(0, 255, step):
				pixels.fill((r, g, b))
			for b in range(255, 0, -step):
				pixels.fill((r, g, b))
		for g in range(255, 0, -step):
			pixels.fill((r, g, b))
			for b in range(0, 255, step):
				pixels.fill((r, g, b))
			for b in range(255, 0, -step):
				pixels.fill((r, g, b))
'''
