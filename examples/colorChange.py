# picks a random color and displays it
# when the button is pressed, takes a few seconds to smoothly change to a new random color
import time
import random
from adafruit_circuitplayground import cp

def _lerp(a, b, frac):
    '''
    "lerp" is short for "linear interpolation".
    This is a helper function that linearly interpolates between two numbers, a and b, based on
    a fraction that goes from 0-1.
    '''
    if frac <= 0:
        return a
    elif frac >= 1:
        return b
    else:
        return a + (b - a) * frac

class ColorLerp:
    '''
    This class expects two colors as tuples (r, g, b) that form the endpoints.
    At time 0, the color is "start"; at time duration, the color is "end".
    The value is a new color that is between them interpolation based on time.
    '''
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.duration = duration
        # when we create this, we start the time as "now"
        self.restart()

    def restart(self):
        "Restarts the lerp at the current time."
        self.start_time = time.monotonic()
        self.end_time = self.start_time + self.duration

    def value(self):
        'Returns a color tuple corresponding to the current time.'
        now = time.monotonic()
        # calculate the fraction that we should use.
        # the _lerp function does the right thing even if we're outside the range
        frac = (now - self.start_time) / self.duration
        return (_lerp(self.start[0], self.end[0], frac),
                _lerp(self.start[1], self.end[1], frac),
                _lerp(self.start[2], self.end[2], frac))

    def done(self):
        "Returns true when the current time is past the end time."
        return time.monotonic() >= self.end_time

    def lerp_to(self, col):
        """
        Sets the start color to the current value, and the end color to col. It
        then restarts.
        """
        self.start = self.value()
        self.end = col
        self.restart()

def randomColor(vmax=255):
    """
    A helper function that returns a random color in the range of 0 to vmax. The
    colors usually look better if one element is zero, so we generate a random
    color with 3 elements, and then set one random element of that color to 0.
    """
    c = [random.randint(0, vmax), random.randint(0, vmax), random.randint(0, vmax)]
    ix = random.randint(0, 2)
    c[ix] = 0
    return c

# this doesn't look good unless we dim the pixels
cp.pixels.brightness = .1
# pick a couple of random colors to start
cstart = randomColor()
cend = randomColor()
# and set up the lerper
lerper = ColorLerp(cstart, cend, 3)
while True:
    # this just lets us turn it off
    if cp.switch:
        cp.pixels.fill((0, 0, 0))
        continue

    # whenever we hit a button, pick a new color and restart
    if cp.button_a:
        lerper.lerp_to(randomColor())

    cp.pixels.fill(lerper.value())
