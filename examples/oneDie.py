# simulates a 6- or 10-sided die roll on the Circuit Playground Express;
# button A is 6-sided (green) and button B is 10-sided (blue);
# the die rolls for a while and then settles on a face.
import time
import random

import board
from adafruit_circuitplayground import cp

stop_delay = 3.0 # sec
start_dwell = 0.050 # 50 msec
dwell_increase = 1 # multiplier
rolling_color = 0x800000
final_6 = 0x008000
final_10 = 0x000080
final_color = final_6

start_time = time.monotonic()
dwell_time = start_dwell
last_dwell = start_time
num_faces = 6

die_faces = {
    1: [2],
    2: [2,7],
    3: [0, 4, 7],
    4: [1, 3, 6, 8],
    5: [1, 3, 5, 7, 9],
    6: [0, 2, 4, 5, 7, 9],
    7: [0, 2, 4, 5, 6, 8, 9],
    8: [0, 1, 3, 4, 5, 6, 8, 9],
    9: [0, 1, 3, 4, 5, 6, 7, 8, 9],
    10: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
}

last_die = 0
last_col = 0
def display_die(n, col):
    global last_die, last_col
    if n == last_die and col == last_col:
        return
    last_die = n
    last_col = col
    cp.pixels.fill(0)
    for ix in die_faces[n]:
        cp.pixels[ix] = col


print("die roller")
r = 1
while True:
    t = time.monotonic()

    if cp.button_a:
        start_time = t
        last_dwell = t
        dwell_time = start_dwell
        num_faces = 6
        final_color = final_6

    if cp.button_b:
        start_time = t
        last_dwell = t
        dwell_time = start_dwell
        num_faces = 10
        final_color = final_10

    # after a while, turn off the LEDs
    if t > start_time + 3*stop_delay:
        cp.pixels.fill(0)

    # if we're past stop_delay from start_time, don't do anything else
    if t > start_time + stop_delay:
        display_die(r, final_color)
        continue

    if t - last_dwell > dwell_time:
        dwell_time *= dwell_increase
        last_dwell = t
        r = random.randint(1, num_faces)
        display_die(r, rolling_color)
