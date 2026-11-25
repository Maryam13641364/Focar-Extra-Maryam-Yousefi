# Maryam
# Final Project: Rectangular path with 3-blink LED at corners using focar module

import focar
from time import sleep

START_DELAY = 2

try:
    focar.stop()
    print("Starting rectangular path...")
    sleep(START_DELAY)

    # Drive along the 4 sides of the rectangle
    for corner in range(1, 5):
        print(f"=== Side and Corner {corner} ===")
        
        # 1. Move along the side
        focar.move_forward()
        
        # 2. Flash LED 3 times at the corner
        focar.blink_led(3)
        
        # 3. Turn 90 degrees (skip turn on the 4th corner to return to start)
        if corner < 4:
            focar.turn_left()

    print("Rectangular path and LED sequence completed successfully!")

finally:
    focar.stop()
    if focar.led:
        focar.led.value(0)
