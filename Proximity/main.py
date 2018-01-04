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

while True:
    print('Proximity: {}'.format(proximity.value))
    if proximity.value > 20000:
        pixels.fill((0, 255, 0))
    else:
        pixels.fill((0, 0, 0))

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
