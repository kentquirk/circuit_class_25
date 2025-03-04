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

def map(x, in_min, in_max, out_min, out_max):
    """
    Map a value from one range to another
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(x, min, max):
    """
    Clamp a value to a range
    """
    return max if x > max else min if x < min else x

class ServoController:
    def __init__(self, servoName, pin=board.A3, anglemin=0, anglemax=180):
        self.servo = servoName
        self.pin = pin
        self.dutymin = servos[servoName]["dutymin"]
        self.dutymax = servos[servoName]["dutymax"]
        self.step = servos[servoName]["step"]
        self.frequency = servos[servoName]["frequency"]
        self.dutyrange = self.dutymax - self.dutymin
        self.anglemin = anglemin
        self.anglemax = anglemax
        self.enabled = False
        self.pwm = None
        self.angle = (self.anglemax + self.anglemin) // 2
        self.step = (self.anglemax - self.anglemin) // 10

    def enable(self):
        self.pwm = pwmio.PWMOut(self.pin, frequency=self.frequency, duty_cycle=0) # we won't be running the PWM until this is nonzero
        self.enabled = True

    def disable(self):
        self.pwm.duty_cycle = 0
        self.pwm.deinit()
        self.enabled = False

    def set(self, angle):
        """
        Angle is a value between anglemin and anglemax, will be clamped
        """
        if not self.enabled:
            raise Exception("Servo not enabled")
        self.angle = clamp(angle, self.anglemin, self.anglemax)
        duty = map(self.angle, self.anglemin, self.anglemax, self.dutymin, self.dutymax)
        print("angle: {} -> duty: {}".format(self.angle, duty))
        self.pwm.duty_cycle = int(duty)

    def up(self):
        if not self.enabled:
            raise Exception("Servo not enabled")
        self.set(self.angle + self.step)

    def down(self):
        if not self.enabled:
            raise Exception("Servo not enabled")
        self.set(self.angle - self.step)

    def test(self):
        if not self.enabled:
            raise Exception("Servo not enabled")
        angle = self.angle
        self.set(self.anglemin)
        time.sleep(1)
        self.set(self.anglemax)
        time.sleep(1)
        self.set(angle)

servo = "TowerPro 9g"
# servo = "HITEC HS-300"

controller = ServoController(servo, anglemin=0, anglemax=180)
controller.enable()
controller.test()

angle = (controller.anglemax + controller.anglemin) // 2


while True:
    if cp.button_a:
        controller.down()
    if cp.button_b:
        controller.up()
    time.sleep(.03)
