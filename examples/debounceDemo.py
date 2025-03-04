# Computers are so fast that they can actually observe the metal contacts of a switch
# bouncing while the switch is pressed and released. This demonstrates that, and
# a technique for "debouncing" switches.

import time
from adafruit_circuitplayground import cp

pixelColor = (255, 0, 0)  # red
currentPixel = 0

class Button:
    def __init__(self, getValueFunc):
        self.f = getValueFunc
        self.lastValue = self.f()
        self.changed = False

    def state(self):
        st = self.f()
        if self.lastValue != st:
            self.changed = True
        return st

    def pressed(self):
        pressed = self.changed and self.lastValue
        self.changed = False
        return pressed

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


    def released(self):
        # if the switch has changed from True to False since the
        # last time, this returns True.
        self.state()
        pressed = self.changed and not self.lastValue
        self.changed = False
        return pressed

def get_button_a():
    # this function returns the current state of button a
    return cp.button_a
def get_button_b():
    # this function returns the current state of button b
    return cp.button_b

button_a = Button(get_button_a)
button_b = Debouncer(get_button_b, .2)

cp.pixels.brightness = .1
cp.pixels.auto_write = False
while True:
    # not debounced, we'll spin one way (fast!)
    changed = False
    if button_a.pressed:
        currentPixel = (currentPixel + 1) % 10
        changed = True

    # debounced, so we can spin the other way with one per tick
    if button_b.pressed:
        currentPixel = (currentPixel - 1) % 10
        changed = True

    # if we changed, set the pixel
    if changed:
        cp.pixels.fill(0)
        cp.pixels[currentPixel] = pixelColor
        cp.pixels.show()
