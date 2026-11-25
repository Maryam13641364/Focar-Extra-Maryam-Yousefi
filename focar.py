from machine import Pin, PWM
from time import sleep

# Motor A (right wheel)
e1 = PWM(Pin(28))
m1 = Pin(27, Pin.OUT)

# Motor B (left wheel)
e2 = PWM(Pin(26))
m2 = Pin(22, Pin.OUT)

e1.freq(1000)
e2.freq(1000)

# Setting LED for Pico W
try:
    led = Pin("LED", Pin.OUT)
except:
    try:
        led = Pin(25, Pin.OUT)
    except:
        led = None

# Motion parameters
SPEED       = 40000  
TURN_SPEED  = 35000  
START_DUTY  = 20000  
TRIM_B      = 1.00   
SIDE_TIME   = 2.5
TURN_TIME   = 0.45   
RAMP_SIDE   = 0.5    
RAMP_TURN   = 0.25   
PAUSE       = 0.2    

def stop():
    # Stop both motors completely
    e1.duty_u16(0)
    e2.duty_u16(0)

def set_duty(duty_a, duty_b, s):
    # Smooth acceleration factor
    e1.duty_u16(int(START_DUTY + (duty_a - START_DUTY) * s))
    e2.duty_u16(int(START_DUTY + (duty_b - START_DUTY) * s))

def smooth_move(dir_a, dir_b, duty_a, duty_b, hold, ramp):
    # S-curve smooth acceleration and deceleration
    m1.value(dir_a)
    m2.value(dir_b)
    steps = max(1, int(ramp * 50))
    for i in range(steps + 1):            
        t = i / steps
        set_duty(duty_a, duty_b, t * t * (3 - 2 * t))
        sleep(ramp / steps)
    sleep(hold)                           
    for i in range(steps, -1, -1):        
        t = i / steps
        set_duty(duty_a, duty_b, t * t * (3 - 2 * t))
        sleep(ramp / steps)
    stop()
    sleep(PAUSE)

def move_forward():
    # Drive forward along a side
    duty_b = min(65535, SPEED * TRIM_B)
    smooth_move(1, 1, SPEED, duty_b, SIDE_TIME, RAMP_SIDE)

def turn_left():
    # Turn left 90 degrees in place
    smooth_move(1, 0, TURN_SPEED, TURN_SPEED, TURN_TIME, RAMP_TURN)

def blink_led(times=3):
    # Flash LED specified times at corners
    print("Flashing LED 3 times...")
    for _ in range(times):
        if led:
            led.value(1)
        sleep(0.4)
        if led:
            led.value(0)
        sleep(0.4)
