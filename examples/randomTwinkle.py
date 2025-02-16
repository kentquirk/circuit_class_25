# randomly lights up individual pixels so the CP twinkles.
import time
import random
import board
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.1
cp.pixels.auto_write = False
v = 0
while True:
    v = random.randint(0, 1024)
    for i in range(10):
        ix = 1 << i
        if v & ix:
            cp.pixels[i] = (0, 0, 16)
        else:
            cp.pixels[i] = 0
    cp.pixels.show()
    time.sleep(0.05)
