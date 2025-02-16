# simple LED counter for Circuit Playground Express
import time
import random
import board
from adafruit_circuitplayground import cp

# expects two colors as tuples (r, g, b), value is a new color that is a linear interpolation based on time
class ColorLerp:
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.duration = duration
        self.start_time = time.monotonic()
        self.end_time = self.start_time + duration

    def value(self):
        now = time.monotonic()
        if now >= self.end_time:
            return self.end
        frac = (now - self.start_time) / self.duration
        return (self.start[0] + (self.end[0] - self.start[0]) * frac,
                self.start[1] + (self.end[1] - self.start[1]) * frac,
                self.start[2] + (self.end[2] - self.start[2]) * frac)

    def done(self):
        return time.monotonic() >= self.end_time

    def reset(self):
        self.start_time = time.monotonic()
        self.end_time = self.start_time + self.duration

def shuffle(a):
    n = len(a)
    for i in range(n):
        j = random.randint(0, n - 1)
        a[i], a[j] = a[j], a[i]

def randomColor():
    # c = [random.randint(0, 60), random.randint(0, 10), random.randint(0, 10)]
    c = [random.randint(0, 40), random.randint(0, 40), 0]
    # c = [random.randint(0, 60), 0, 0]
    shuffle(c)
    return c

v = 0
cstart = randomColor()
cend = randomColor()
lerp = ColorLerp(cstart, cend, 3)
while True:
    if cp.switch:
        cp.pixels.fill((0, 0, 0))
        continue

    if lerp.done():
        cstart = cend
        cend = randomColor()
        lerp = ColorLerp(cstart, cend, 3)
    cp.pixels.fill(lerp.value())
    time.sleep(0.01)
