import focar

# complete round
for i in range(4):
    focar.move_forward(2)
    focar.stop()
    
# wrinkling 3 times at the corners
    focar.blink_led(3)  
    focar.turn_right()
