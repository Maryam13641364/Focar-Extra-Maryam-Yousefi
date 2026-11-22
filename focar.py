import time

def move_forward(seconds):
    print("Robot moving forward...")
    time.sleep(seconds)

def stop():
    print("Robot stopped.")

def turn_right(degrees=90):
    print("Robot turning 90 degrees right...")
    time.sleep(1)

def blink_led(times=3):
    print(f"Blinking LED {times} times...")
    for _ in range(times):
        time.sleep(0.5)
        time.sleep(0.5)
