# uses the accelerometer to make a simple "level".
# If the board is level, all the pixels will be white;
# if it's tilted to one side, the pixels on the high side
# will be blue and the pixels on the low side will be red.
from adafruit_circuitplayground import cp

highside = 0x0000FF
lowside = 0xFF0000
green = 0x00FF00
off = 0x0
level = 0xFFFFFF

xlo = [2]
xhi = [7]
ylo = [4, 5]
yhi = [0, 9]
others = [1, 3, 6, 8]

cp.pixels.brightness = 0.1

def clearPixels():
    for p in range(10):
        cp.pixels[p] = 0

def setPixels(pixels, col):
    for p in pixels:
        cp.pixels[p] = col

while True:
    acc = [int(a) for a in cp.acceleration]
    x, y, z = acc
    if cp.button_a:
        print(x, y, z)

    if x > 0:
        setPixels(xlo, lowside)
        setPixels(xhi, highside)
    elif x < 0:
        setPixels(xlo, highside)
        setPixels(xhi, lowside)
    else:
        setPixels(xlo, level)
        setPixels(xhi, level)

    if y > 0:
        setPixels(ylo, lowside)
        setPixels(yhi, highside)
    elif y < 0:
        setPixels(ylo, highside)
        setPixels(yhi, lowside)
    else:
        setPixels(ylo, level)
        setPixels(yhi, level)


    if x == 0 and y == 0:
        setPixels(others, green)
    else:
        setPixels(others, off)
