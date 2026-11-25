# Maryam
# 25.11.2026
# extra assignment2
# Square path with soft starts and soft stops
# The videos show that this turn goes to the LEFT, so it is called turn_left.
# Every move speeds up and slows down smoothly.
# 3 times flashing at each corner

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

# setting LED
try:
    led = Pin("LED", Pin.OUT)
except:
    try:
        led = Pin(25, Pin.OUT)
    except:
        led = None

# setting movements
SPEED       = 40000  
TURN_SPEED  = 35000  
START_DUTY  = 20000  
TRIM_B      = 1.00   

# time of moving
SIDE_TIME   = 2.5
# time of turning 90 degrees    
TURN_TIME   = 0.45   

# Motion and Ramp Configuration 
# Ramp time for straight sides in seconds
RAMP_SIDE   = 0.5 
# Ramp time for turning actions in seconds   
RAMP_TURN   = 0.25 
# Short pause time between movements  
PAUSE       = 0.2 
# delay before starting the routine   
START_DELAY = 2      


def stop():
    # Sets PWM duty cycle to 0 for both motors to halt movement completely
    e1.duty_u16(0)
    e2.duty_u16(0)


def set_duty(duty_a, duty_b, s):
    # Applies an interpolation factor 's' between START_DUTY and target duty for smooth acceleration
    e1.duty_u16(int(START_DUTY + (duty_a - START_DUTY) * s))
    e2.duty_u16(int(START_DUTY + (duty_b - START_DUTY) * s))


def smooth_move(dir_a, dir_b, duty_a, duty_b, hold, ramp):
    # Set motor direction pins
    m1.value(dir_a)
    m2.value(dir_b)
    # Calculate step count based on ramp duration
    steps = max(1, int(ramp * 50))
    # Soft start (acceleration phase using cubic smoothstep formula)
    for i in range(steps + 1):            
        t = i / steps
        set_duty(duty_a, duty_b, t * t * (3 - 2 * t))
        sleep(ramp / steps)
        # Hold full speed / duration for the movement
    sleep(hold) 
    # Soft stop (deceleration phase)                          
    for i in range(steps, -1, -1):        
        t = i / steps
        set_duty(duty_a, duty_b, t * t * (3 - 2 * t))
        sleep(ramp / steps)
        # Complete stop and brief pause after movement
    stop()
    sleep(PAUSE)


def forward():
    # Adjust right wheel speed (duty_b) according to the trim factor to maintain a straight line
    duty_b = min(65535, SPEED * TRIM_B)
    # Execute smooth move for driving forward (both motors moving forward: 1, 1)
    smooth_move(1, 1, SPEED, duty_b, SIDE_TIME, RAMP_SIDE)


def turn_left():
    # Execute smooth move for a pivot turn in place (motors moving in opposite directions: 1, 0)
    smooth_move(1, 0, TURN_SPEED, TURN_SPEED, TURN_TIME, RAMP_TURN)


def flash_led():
    # flashing 3 times
    print("Flashing LED 3 times...")
    for i in range(3):
        if led:
            # LED on
            led.value(1)
        sleep(0.4) 
        # LED off    
        if led:
            led.value(0) 
        sleep(0.4)


# main movements
try:
    stop()
    print("Starting rectangular path...")
    sleep(START_DELAY)

    for corner in range(1, 5):
        print(f"=== Side and Corner {corner} ===")
        
        # ۱.compelet movement in each side
        forward()
        
        # ۲. flashing 3 times in the corner
        flash_led()
        
        # ۳. turning 90 degrees
        if corner < 4:
            turn_left()

    print("Rectangular path and LED sequence completed successfully!")

finally:
    stop()
    if led:
        led.value(0)
