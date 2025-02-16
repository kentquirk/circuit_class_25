# LED counter for Circuit Playground Express
# with a demonstration of the "auto_write" feature
# of the pixels; it's convenient but a lot slower
# if you're setting most of the pixels each time.
import time
import board
from adafruit_circuitplayground import cp

count = 0
start = time.monotonic()
cp.pixels.brightness = 0.1
while True:
    cp.pixels.auto_write = cp.switch
    count += 1
    for i in range(10):
        ix = 1 << i
        if count & ix:
            cp.pixels[i] = 0xff_00_00
        else:
            cp.pixels[i] = 0
    if not cp.switch:
        cp.pixels.show()
    if count == 1024:
        count = 0
        duration = time.monotonic() - start
        print(duration, "seconds")
        start = time.monotonic()