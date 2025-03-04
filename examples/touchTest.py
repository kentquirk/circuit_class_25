# demonstration script to show some of what the Circuit Python device can do

# We're going to spin a colored dot around the ring of LEDs
# the color of the dot can be changed by tapping the touch pads
# the direction of the spin can be changed by flipping the switch
# the speed can be changed by pressing either button
# it can be turned off by pressing both buttons at once

import time
from adafruit_circuitplayground import cp

pixelColor = 0xFF0000  # red
direction = 1
dwell = 0.1  # how long to wait between moves
lasttick = time.monotonic()
currentPixel = 0

class Debouncer:
    """
    This is a class to help in 'debouncing' hardware. The computers are so fast that
    switches can change values a lot more often than it looks.
    """
    def __init__(self, getValueFunc, debounceTime):
        self.f = getValueFunc
        self.debounceTime = debounceTime
        self.lastValue = self.f()
        self.waitUntil = time.monotonic()
        self.changed = False

    def state(self):
        now = time.monotonic()
        if now < self.waitUntil:
            return self.lastValue
        st = self.f()
        if st != self.lastValue:
            self.waitUntil = now + self.debounceTime
            self.lastValue = st
            self.changed = True
        return st

    def pressed(self):
        self.state()
        pressed = self.changed and self.lastValue
        self.changed = False
        return pressed


# we need to wrap these properties in functions so we can pass them to the Debouncer
def get_button_a():
    return cp.button_a

def get_button_b():
    return cp.button_b


button_a = Debouncer(get_button_a, .2)
button_b = Debouncer(get_button_b, .2)

while True:
    t = time.monotonic()
    if t > lasttick + dwell:
        currentPixel += direction
        if currentPixel < 0:
            currentPixel = 9
        if currentPixel > 9:
            currentPixel = 0
        lasttick = t
        cp.pixels.fill(0)
        cp.pixels[currentPixel] = pixelColor

    if cp.switch:
        direction = -1
    else:
        direction = 1

    if button_a.pressed():
        print("slowing down")
        dwell *= 2
        if dwell > 1.0:
            dwell = 1.0

    if button_b.pressed():
        print("speeding up")
        dwell /= 2
        if dwell < 0.01:
            dwell = 0.01

    if button_a.state() and button_b.state():
        # both pressed, "shut off"
        pixelColor = 0

    if cp.touch_A1:
        pixelColor = 0xFF0000  # red
    elif cp.touch_A2:
        pixelColor = 0x00FF00  # green
    elif cp.touch_A3:
        pixelColor = 0x0000FF  # blue
    elif cp.touch_A4:
        pixelColor = 0xFFFF00  # yellow
    elif cp.touch_A5:
        pixelColor = 0xFF00FF  # magenta
    elif cp.touch_A6:
        pixelColor = 0x00FFFF  # cyan

