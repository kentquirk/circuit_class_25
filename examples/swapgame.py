# implements a simple game
# there are 5 LEDs in a pattern of 5 colors
# red, white, blue, green, yellow
# there are 5 leds you need to make match the pattern
# same colors, different order.
# there are 4 pads you can touch for different transformations


import time
import random
from adafruit_circuitplayground import cp

colors = [
    (255, 0, 0),
    (255, 255, 255),
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
]

class SwapGame:
    def __init__(self, nswaps=5):
        cp.pixels.brightness = .1
        cp.pixels.auto_write = False
        self.target = [0, 1, 2, 3, 4]
        self.current = [0, 1, 2, 3, 4]
        self.nswaps = nswaps
        self.scramble(nswaps)
        self.display()

    def swap(self, n):
        s = self.current
        if n == 0:
            # 12345 -> 21354
            s[0], s[1] = s[1], s[0]
            s[3], s[4] = s[4], s[3]
        elif n == 1:
            # 12345 -> 52143
            s[0], s[2], s[4] = s[2], s[4], s[0]
        elif n == 2:
            # 12345 -> 14325
            s[1], s[3] == s[3], s[1]
        else:
            # 12345 -> 23451
            s[0], s[1], s[2], s[3], s[4] = s[1], s[2], s[3], s[4], s[0]

    def scramble(self, n=0):
        if n == 0:
            n = self.nswaps
        self.current = self.target[:]
        for i in range(n):
            self.swap(random.randint(0, 4))

    def won(self):
        return self.current == self.target

    def display(self):
        for i in range(5):
            cp.pixels[i] = colors[self.target[i]]
            cp.pixels[9-i] = colors[self.current[i]]
        cp.pixels.show()

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

game = SwapGame(nswaps=1)

button_a = Debouncer(lambda: cp.button_a, 0.25)
t1 = Debouncer(lambda: cp.touch_A1, 0.25)
t2 = Debouncer(lambda: cp.touch_A2, 0.25)
t3 = Debouncer(lambda: cp.touch_A3, 0.25)
t4 = Debouncer(lambda: cp.touch_A4, 0.25)

while True:
    # this just lets us turn it off
    if cp.switch:
        cp.pixels.fill((0, 0, 0))
        cp.pixels.show()
        continue

    if button_a.pressed():
        game.scramble()
    if t1.pressed():
        game.swap(0)
    if t2.pressed():
        game.swap(1)
    if t3.pressed():
        game.swap(2)
    if t4.pressed():
        game.swap(3)

    game.display()

    if game.won():
        cp.pixels.brightness == .5
        for i in range(4):
            time.sleep(.5)
            cp.pixels.brightness = 0
            cp.pixels.show()
            time.sleep(.5)
            cp.pixels.brightness == .5
            cp.pixels.show()
        cp.pixels.brightness = .1
        game.scramble()
