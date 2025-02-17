---
marp: true
class: invert
---

![bg contain right](images/cp.png)

# Notes on Random topics
## Circuit Playground Class for Spark Makerspace
## Kent Quirk, Feb-Mar 2025

---

# NeoPixels

* Smart LEDs
* Each has an address, and they're connected end-to-end serially. You can put thousands on one string.
* It takes time to move information along the chain.
* Simply writing an integer or tuple to `cp.pixels[4]` sets its value (where 4 is the number of the pixel you want to set)
* But if you set a bunch, use `cp.pixels.auto_write=False` and then `cp.pixels.show()` to write them all at once -- it's literally 10x faster.

---

# Servos

* Position of the servo is based on the duty cycle of the incoming signal.
* PWM == Pulse Width Modulation
* These chips can do that really cheaply

---

# Infrared (IR) Remote Send & Receive

* Standard IR signals are pulses of a carrier signal (usually around 40 KHz)
* Different manufacturers use different pulse patterns
* There's a s