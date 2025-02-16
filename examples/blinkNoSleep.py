# simple LED counter for Circuit Playground Express
import time
import random
import board
from adafruit_circuitplayground import cp

while True:
    t = time.monotonic()
    cp.red_led = int(2*t) % 2   # 1,0,1,0...
