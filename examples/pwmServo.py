# implements a simple game
# there are 5 LEDs in a pattern of 5 colors
# red, white, blue, green, yellow
# there are 5 leds you need to make match the pattern
# same colors, different order.
# there are 4 pads you can touch for different transformations


# Write your code here :-)
import pwmio
import board
import time
from adafruit_circuitplayground import cp

servos = {
    "TowerPro 9g": {
        "dutymin": 1800,
        "dutymax": 8400,
        "step": 150,
        "frequency": 50,
    },
    "HITEC HS-300": {
        "dutymin": 4600,
        "dutymax": 16000,
        "step": 100,
        "frequency": 100,
    },
}

# servo = "TowerPro 9g"
servo = "HITEC HS-300"


dutymin = servos[servo]["dutymin"]
dutymax = servos[servo]["dutymax"]
step = servos[servo]["step"]
frequency = servos[servo]["frequency"]
dutyrange = dutymax - dutymin

pwm = pwmio.PWMOut(board.A3, frequency=frequency, duty_cycle=0) # we won't be running the PWM until this is nonzero
duty = (dutymax + dutymin) // 2
pwm.duty_cycle = dutymin
time.sleep(1)
pwm.duty_cycle = dutymax
time.sleep(1)
pwm.duty_cycle = duty
while True:
    if cp.button_a:
        duty -= step
    if cp.button_b:
        duty += step
    if duty < dutymin:
        duty = dutymin
    if duty > dutymax:
        duty = dutymax
    print(duty)
    pwm.duty_cycle = duty
    time.sleep(.03)
