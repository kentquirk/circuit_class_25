# simple LED counter for Circuit Playground Express
import time
import random
import board
from adafruit_circuitplayground import cp

v = 0
while True:
    v = random.randint(0, 1024)
    for i in range(10):
        ix = 1 << i
        if v & ix:
            cp.pixels[i] = (0, 0, 16)
        else:
            cp.pixels[i] = 0
